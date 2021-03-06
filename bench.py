#!/usr/bin/env python3

from logtree import LogTree
import csv
import random
import itertools as it
import sys

def order_in_order(n, case='appends'):
    if case == 'deletes':
        return list(it.repeat(0, n))
    else:
        return range(n)

def order_reversed(n, case='appends'):
    if case == 'creates':
        return list(it.repeat(0, n))
    else:
        return reversed(range(n))

def order_random(n, case='appends'):
    if case == 'creates':
        return list(random.randrange(x+1) for x in range(n))
    elif case in {'deletes'}:
        return list(random.randrange(x+1) for x in reversed(range(n)))
    else:
        x = list(range(n))
        random.shuffle(x)
        return x

def order_in_order_then_reversed(n, case='appends'):
    if case in {'updates', 'removes', 'deletes'}:
        return order_reversed(n)
    else:
        return order_in_order(n)

def order_reversed_then_in_order(n, case='appends'):
    if case in {'updates', 'removes', 'deletes'}:
        return order_in_order(n)
    else:
        return order_reversed(n)

ORDERS = {
    'random':                   order_random,
    'in_order':                 order_in_order,
    'reversed':                 order_reversed,
    'in_order_then_reversed':   order_in_order_then_reversed,
    'reversed_then_in_order':   order_reversed_then_in_order,
}

def main(case, order, path, N=10000, step=10):
    N = int(N)
    step = int(step)
    with open(path, 'a') as f:
        w = csv.writer(f)
        w.writerow(['case', 'order', 'n',
            'avg_iters', 'min_iters', 'max_iters',
            'avg_iters2', 'min_iters2', 'max_iters2',
            'avg_height', 'min_height', 'max_height'])

        for n in range(step, N, step):
            print("running %s + %s for n=%r" % (case, order, n))
            if case == 'appends':
                baseline = {}
                iters = []
                iters2 = []
                tree = LogTree()
                for i in ORDERS[order](n):
                    tree.iters = 0
                    tree.iters2 = 0
                    tree.append(i, repr(i))
                    iters.append(tree.iters)
                    iters2.append(tree.iters2)
                    baseline[i] = repr(i)
                heights = list(tree.heights())

                for i in ORDERS[order](n):
                    if tree.lookup(i) != baseline.get(i):
                        print('failed %s + %s for n=%r, could not find %r' % (
                            case, order, n, i))
                        sys.exit(1)

            elif case == 'lookups':
                baseline = {}
                iters = []
                iters2 = []
                tree = LogTree()
                for i in ORDERS[order](n):
                    tree.append(i, repr(i))
                    baseline[i] = repr(i)

                for i in ORDERS[order](n):
                    tree.iters = 0
                    tree.iters2 = 0
                    v = tree.lookup(i)
                    iters.append(tree.iters)
                    iters2.append(tree.iters2)
                    if v != baseline.get(i):
                        print('failed %s + %s for n=%r, could not find %r' % (
                            case, order, n, i))
                        sys.exit(1)
                heights = list(tree.heights())

            elif case == 'traversal':
                baseline = {}
                iters = []
                iters2 = []
                tree = LogTree()
                for i in ORDERS[order](n):
                    tree.append(i, repr(i))
                    baseline[i] = repr(i)

                tree.iters = 0
                tree.iters2 = 0
                traversal = []
                for k, v in tree.traverse():
                    traversal.append((k, v))
                    iters.append(tree.iters)
                    iters2.append(tree.iters2)
                    tree.iters = 0
                    tree.iters2 = 0
                heights = list(tree.heights())

                for k, v in traversal:
                    if v != baseline.get(k):
                        print('failed %s + %s for n=%r, could not find %r' % (
                            case, order, n, k))
                        sys.exit(1)

            elif case == 'updates':
                baseline = {}
                iters = []
                iters2 = []
                tree = LogTree()
                for i in ORDERS[order](n):
                    tree.append(i, 'bad')
                    baseline[i] = 'bad'

                for i in ORDERS[order](n, 'updates'):
                    tree.iters = 0
                    tree.iters2 = 0
                    tree.append(i, repr(i))
                    iters.append(tree.iters)
                    iters2.append(tree.iters2)
                    baseline[i] = repr(i)
                heights = list(tree.heights())

                for i in ORDERS[order](n):
                    if tree.lookup(i) != baseline.get(i):
                        print('failed %s + %s for n=%r, could not find %r' % (
                            case, order, n, i))
                        sys.exit(1)

            elif case == 'removes':
                baseline = {}
                iters = []
                iters2 = []
                tree = LogTree()
                for i in ORDERS[order](n):
                    tree.append(i, 'bad')
                    baseline[i] = 'bad'

                for i in ORDERS[order](n, 'removes'):
                    tree.iters = 0
                    tree.iters2 = 0
                    tree.remove(i)
                    iters.append(tree.iters)
                    iters2.append(tree.iters2)
                    del baseline[i]
                heights = list(tree.heights())

                for i in ORDERS[order](n):
                    if tree.lookup(i) != baseline.get(i):
                        print('failed %s + %s for n=%r, found %r' % (
                            case, order, n, i))
                        sys.exit(1)

            elif case == 'creates':
                # Fun fact! Replicating this behavior with Python's built
                # in data structures takes O(n^2), slower than the actual
                # data structure we're testing. So we use special sequences
                # to make sure the results are nice and packed. More tests
                # in logtree.py
                iters = []
                iters2 = []
                tree = LogTree()
                for i in ORDERS[order](n, 'creates'):
                    tree.iters = 0
                    tree.iters2 = 0
                    tree.create(i, repr(i))
                    iters.append(tree.iters)
                    iters2.append(tree.iters2)
                heights = list(tree.heights())

                for i in ORDERS[order](n):
                    if tree.lookup(i) == None:
                        print('failed %s + %s for n=%r, could not find %r' % (
                            case, order, n, i))
                        sys.exit(1)

            elif case == 'deletes':
                # Similar workaround here with special sequences
                iters = []
                iters2 = []
                tree = LogTree()
                for i in ORDERS[order](n, 'appends'):
                    tree.append(i, repr(i))

                for i in ORDERS[order](n, 'deletes'):
                    tree.iters = 0
                    tree.iters2 = 0
                    tree.delete(i)
                    iters.append(tree.iters)
                    iters2.append(tree.iters2)
                heights = list(tree.heights())

                for i in ORDERS[order](n):
                    if tree.lookup(i) != None:
                        print('failed %s + %s for n=%r, found %r' % (
                            case, order, n, i))
                        sys.exit(1)

            else:
                print("unknown case %r?" % case)
                sys.exit(1)

            w.writerow([case, order, n,
                sum(iters)/len(iters), min(iters), max(iters),
                sum(iters2)/len(iters2), min(iters2), max(iters2),
                sum(heights)/len(heights), min(heights), max(heights)])
            f.flush()

if __name__ == "__main__":
    import sys
    main(*sys.argv[1:])
