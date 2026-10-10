from collections import deque
import sys


def solve_wjp(capacities, initial_state, target, target_jug=None, allow_fill_empty=True):
    """
    Solves the Water Jug Problem using Breadth-First Search (BFS) to guarantee
    the shortest path (minimum number of steps).

    Parameters:
        capacities (tuple): Maximum capacity of each jug.
        initial_state (tuple): Initial amount of water in each jug.
        target (int): Target volume of water to measure.
        target_jug (int, optional): Specific jug index (0-indexed) that must contain the target.
                                    If None, the goal is satisfied if any jug has the target amount.
        allow_fill_empty (bool): Whether filling from/emptying to an external source is allowed.

    Returns:
        list: Sequence of (action_description, state_tuple) steps from start to goal,
              or None if unsolvable.
    """
    initial_state = tuple(initial_state)
    capacities = tuple(capacities)
    n = len(capacities)

    def is_goal(state):
        if target_jug is None:
            return any(val == target for val in state)
        return state[target_jug] == target

    if is_goal(initial_state):
        return [("Initial State", initial_state)]

    queue = deque([(initial_state, [("Initial State", initial_state)])])
    visited = {initial_state}

    while queue:
        current_state, path = queue.popleft()

        # 1. Pour between jugs
        for i in range(n):
            for j in range(n):
                if i != j and current_state[i] > 0 and current_state[j] < capacities[j]:
                    amount = min(current_state[i], capacities[j] - current_state[j])
                    next_state = list(current_state)
                    next_state[i] -= amount
                    next_state[j] += amount
                    next_state = tuple(next_state)

                    if next_state not in visited:
                        visited.add(next_state)
                        action = f"Pour Jug {i + 1} ({capacities[i]}L) -> Jug {j + 1} ({capacities[j]}L) [{amount}L]"
                        new_path = path + [(action, next_state)]
                        if is_goal(next_state):
                            return new_path
                        queue.append((next_state, new_path))

        if allow_fill_empty:
            # 2. Fill a jug from external tap
            for i in range(n):
                if current_state[i] < capacities[i]:
                    next_state = list(current_state)
                    next_state[i] = capacities[i]
                    next_state = tuple(next_state)

                    if next_state not in visited:
                        visited.add(next_state)
                        action = f"Fill Jug {i + 1} ({capacities[i]}L)"
                        new_path = path + [(action, next_state)]
                        if is_goal(next_state):
                            return new_path
                        queue.append((next_state, new_path))

            # 3. Empty a jug completely
            for i in range(n):
                if current_state[i] > 0:
                    next_state = list(current_state)
                    next_state[i] = 0
                    next_state = tuple(next_state)

                    if next_state not in visited:
                        visited.add(next_state)
                        action = f"Empty Jug {i + 1} ({capacities[i]}L)"
                        new_path = path + [(action, next_state)]
                        if is_goal(next_state):
                            return new_path
                        queue.append((next_state, new_path))

    return None


def format_state(state, capacities):
    """Format state as e.g. 12/12 0/8 0/5."""
    return " ".join(f"{amt}/{cap}" for amt, cap in zip(state, capacities))


def print_solution(title, capacities, initial_state, target, target_jug=None, allow_fill_empty=True):
    print("=" * 70)
    print(f"{title}")
    print("=" * 70)
    print(f"Jugs Capacities : {capacities}")
    print(f"Initial State   : {format_state(initial_state, capacities)}")
    target_desc = f"Target {target}L in any jug" if target_jug is None else f"Target {target}L in Jug {target_jug + 1}"
    print(f"Target          : {target_desc}")
    print(f"Operations      : {'Pour, Fill, Empty' if allow_fill_empty else 'Pour only (closed system)'}")
    print("-" * 70)

    solution = solve_wjp(
        capacities=capacities,
        initial_state=initial_state,
        target=target,
        target_jug=target_jug,
        allow_fill_empty=allow_fill_empty,
    )

    if not solution:
        print("No solution found.")
        print()
        return

    for step_num, (action, state) in enumerate(solution):
        state_str = format_state(state, capacities)
        if step_num == 0:
            print(f"Step {step_num:2d}: {action:<45} -> State: {state_str}")
        else:
            print(f"Step {step_num:2d}: {action:<45} -> State: {state_str}")

    print("-" * 70)
    print(f"Goal reached in {len(solution) - 1} step(s)!")
    print()


def parse_input_string(text):
    """
    Parses strings like '12/12 0/8 0/5 target : 4' or '0/6 0/8 0/5 : target 5'.
    Returns (capacities, initial_state, target).
    """
    parts = text.strip().split()
    jug_tokens = []
    target = None

    i = 0
    while i < len(parts):
        token = parts[i]
        if "/" in token:
            amt_str, cap_str = token.split("/")
            jug_tokens.append((int(amt_str), int(cap_str)))
        elif "target" in token.lower():
            # next token might be ':' or the number directly
            i += 1
            if i < len(parts) and parts[i] == ":":
                i += 1
            if i < len(parts):
                target = int(parts[i].replace(":", ""))
        i += 1

    if not jug_tokens or target is None:
        raise ValueError("Invalid format. Expected e.g. '12/12 0/8 0/5 target: 4'")

    initial_state = tuple(amt for amt, _ in jug_tokens)
    capacities = tuple(cap for _, cap in jug_tokens)
    return capacities, initial_state, target


def main():
    if len(sys.argv) > 1:
        raw_input = " ".join(sys.argv[1:])
        try:
            capacities, initial_state, target = parse_input_string(raw_input)
            allow_fill_empty = (sum(initial_state) == 0 or any(c not in initial_state for c in capacities))
            print_solution("Custom Problem Instance", capacities, initial_state, target, allow_fill_empty=allow_fill_empty)
            return
        except Exception as e:
            print(f"Error parsing argument: {e}")
            print("Running default cases instead...\n")

    # Case 1: 12/12 0/8 0/5 target : 4
    print_solution(
        title="Case 1: 12/12 0/8 0/5 | Target: 4",
        capacities=(12, 8, 5),
        initial_state=(12, 0, 0),
        target=4,
        allow_fill_empty=True,
    )

    # Case 1 (Pour Only / Decanting variant for comparison)
    print_solution(
        title="Case 1 (Variant: Target 4 in Jug 3 with Pour only)",
        capacities=(12, 8, 5),
        initial_state=(12, 0, 0),
        target=4,
        target_jug=2,
        allow_fill_empty=False,
    )

    # Case 2: 0/6 0/8 0/5 : target 5
    print_solution(
        title="Case 2: 0/6 0/8 0/5 | Target: 5 (Any Jug)",
        capacities=(6, 8, 5),
        initial_state=(0, 0, 0),
        target=5,
        allow_fill_empty=True,
    )

    # Case 2 (Variant: Target 5 in Jug 1 - 6L jug)
    print_solution(
        title="Case 2 (Variant: Target 5 in Jug 1 [6L Jug])",
        capacities=(6, 8, 5),
        initial_state=(0, 0, 0),
        target=5,
        target_jug=0,
        allow_fill_empty=True,
    )


if __name__ == "__main__":
    main()
