#!/usr/bin/python

import sys
import random

r = random.Random(12345)

NUM_PRISONERS = 23

TEST_CASES = [
  [y for x in range(1, 23) for y in [x, 0]],
  [0] + [y for x in range(1, 23) for y in [x, 0]],
  [0, 0, 0, 0, 0] + [y for x in range(1, 23) for y in [x, x, 0, 0]],
]


def main(args):
    initial_state = 0
    test_case = None

    try:
        initial_state = {'00': 0, '01': 1, '10': 2, '11': 3}[args[0]]

        test_case_no = int(args[1])
        test_case = TEST_CASES[test_case_no]
        print('Using test case #%d.' % test_case_no)
    except:
        pass

    leader = Leader()
    followers = [Follower() for _ in range(1, NUM_PRISONERS)]

    t = 0
    state = initial_state
    print('There are %d prisoners.' % NUM_PRISONERS)
    print('Initial switch state: ' + format(state, '02b'))
    print('   T: SW [P#] DONE')

    while t <= 10000:
        # choose a prisoner
        if test_case is None:
            n = r.randint(0, NUM_PRISONERS - 1)
        else:
            n = test_case[t % len(test_case)]

        # print status
        bitmap = ''.join('-*'[p.visited] for p in [leader] + followers)
        print('%4d: %s [%2d] %s' % (t, format(state, '02b'), n, bitmap))

        if n == 0:
            # the leader's move
            next_state, is_call = leader.move(state)
            if is_call:
                print('#0 makes a call.')
                if all(p.visited for p in followers):
                    print('SUCCESS!!!')
                    return 0
                else:
                    print('FAILURE!!!')
                    return 2
        else:
            # a follower's move
            next_state = followers[n - 1].move(state)
        state = next_state
        t += 1
    return 1


class Leader:
    def __init__(self):
        self.visited = False
        self.counter = 0

    def move(self, state):
        self.visited = True
        if state & 1:
            self.counter += 1
            return state ^ 1, self.counter == NUM_PRISONERS - 1
        else:
            return state ^ 2, False


class Follower:
    def __init__(self):
        self.visited = False
        self.done = False

    def move(self, state):
        self.visited = True
        if self.done or state & 1:
            return state ^ 2
        else:
            self.done = True
            return state ^ 1

sys.exit(main(sys.argv[1:]))
