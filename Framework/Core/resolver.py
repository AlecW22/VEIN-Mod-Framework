from collections import defaultdict
import heapq


class ResolutionResult:
    def __init__(self):
        self.load_order = []
        self.disabled = {}
        self.errors = []


def resolve_load_order(mods):
    result = ResolutionResult()

    active = dict(mods)

    # Disable mods with missing required dependencies
    for mod_id, info in list(active.items()):
        manifest = info["manifest"]

        missing = [
            dependency
            for dependency in manifest.dependencies
            if dependency not in active
        ]

        if missing:
            result.disabled[mod_id] = (
                "Missing required dependencies: "
                + ", ".join(sorted(missing))
            )
            del active[mod_id]

    # Handle declared conflicts
    disabled_by_conflict = set()

    for mod_id, info in active.items():
        manifest = info["manifest"]

        for conflict in manifest.conflicts:
            if conflict in active:
                pair = sorted([mod_id, conflict])

                # Deterministic rule:
                # alphabetically later mod gets disabled
                loser = pair[1]

                result.disabled[loser] = (
                    f"Declared conflict between "
                    f"'{pair[0]}' and '{pair[1]}'"
                )

                disabled_by_conflict.add(loser)

    for mod_id in disabled_by_conflict:
        active.pop(mod_id, None)

    graph = defaultdict(set)
    indegree = {
        mod_id: 0
        for mod_id in active
    }

    def add_edge(before, after):
        if (
            before not in active
            or after not in active
            or before == after
        ):
            return

        if after not in graph[before]:
            graph[before].add(after)
            indegree[after] += 1

    for mod_id, info in active.items():
        manifest = info["manifest"]

        # Required dependencies load first
        for dependency in manifest.dependencies:
            add_edge(dependency, mod_id)

        # loadAfter means target loads before this mod
        for target in manifest.loadAfter:
            add_edge(target, mod_id)

        # loadBefore means this mod loads before target
        for target in manifest.loadBefore:
            add_edge(mod_id, target)

    available = [
        mod_id
        for mod_id, degree in indegree.items()
        if degree == 0
    ]

    heapq.heapify(available)

    ordered = []

    while available:
        current = heapq.heappop(available)
        ordered.append(current)

        for neighbor in sorted(graph[current]):
            indegree[neighbor] -= 1

            if indegree[neighbor] == 0:
                heapq.heappush(
                    available,
                    neighbor
                )

    # If not everything was resolved, there is a cycle
    if len(ordered) != len(active):
        unresolved = sorted(
            mod_id
            for mod_id, degree in indegree.items()
            if degree > 0
        )

        result.errors.append(
            "Circular dependency or load-order relationship "
            f"detected involving: {', '.join(unresolved)}"
        )

        for mod_id in unresolved:
            result.disabled[mod_id] = (
                "Circular dependency/load-order relationship"
            )

        ordered = [
            mod_id
            for mod_id in ordered
            if mod_id not in unresolved
        ]

    result.load_order = ordered

    return result