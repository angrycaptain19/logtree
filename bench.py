#!/usr/bin/env python3

from logtree import LogTree
import csv
import random
import itertools as it
import sys

def order_in_order(n, i=0):
    return range(n)

def order_reversed(n, i=0):
    return reversed(range(n))

def order_random(n, i=0):
    x = list(range(n))
    random.shuffle(x)
    return x

def order_in_order_then_reversed(n, i=0):
    if i == 0:
        return order_in_order(n)
    else:
        return order_in_reversed(n)

def order_reversed_then_in_order(n, i=0):
    if i == 0:
        return order_in_reversed(n)
    else:
        return order_in_order(n)

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
        w.writerow(['case', 'n',
            'max_iters', 'avg_iters',
            'max_iters2', 'avg_iters2',
            'height'])

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

                max_iters = max(iters)
                avg_iters = sum(iters)/len(iters)
                max_iters2 = max(iters2)
                avg_iters2 = sum(iters2)/len(iters2)
                height = tree.height()

                for i in ORDERS[order](n):
                    if tree.lookup(i) != baseline.get(i):
                        print('failed %s + %s for n=%r, could not find %r' % (
                            case, order, n, i))
                        sys.exit(1)
            elif case == 'updates':
                baseline = {}
                iters = []
                iters2 = []
                tree = LogTree()
                for i in ORDERS[order](n):
                    tree.append(i, 'bad')
                    baseline[i] = 'bad'

                for i in ORDERS[order](n):
                    tree.iters = 0
                    tree.iters2 = 0
                    tree.append(i, repr(i))
                    iters.append(tree.iters)
                    iters2.append(tree.iters2)
                    baseline[i] = repr(i)

                max_iters = max(iters)
                avg_iters = sum(iters)/len(iters)
                max_iters2 = max(iters2)
                avg_iters2 = sum(iters2)/len(iters2)
                height = tree.height()

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

                max_iters = max(iters)
                avg_iters = sum(iters)/len(iters)
                max_iters2 = max(iters2)
                avg_iters2 = sum(iters2)/len(iters2)
                height = tree.height()
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

                for k, v in traversal:
                    if v != baseline.get(k):
                        print('failed %s + %s for n=%r, could not find %r' % (
                            case, order, n, k))
                        sys.exit(1)

                max_iters = max(iters)
                avg_iters = sum(iters)/len(iters)
                max_iters2 = max(iters2)
                avg_iters2 = sum(iters2)/len(iters2)
                height = tree.height()
            elif case == 'removes':
                baseline = {}
                iters = []
                iters2 = []
                tree = LogTree()
                for i in ORDERS[order](n):
                    tree.append(i, 'bad')
                    baseline[i] = 'bad'

                for i in ORDERS[order](n):
                    tree.iters = 0
                    tree.iters2 = 0
                    tree.remove(i)
                    iters.append(tree.iters)
                    iters2.append(tree.iters2)
                    del baseline[i]

                max_iters = max(iters)
                avg_iters = sum(iters)/len(iters)
                max_iters2 = max(iters2)
                avg_iters2 = sum(iters2)/len(iters2)
                height = tree.height()

                for i in ORDERS[order](n):
                    if tree.lookup(i) != baseline.get(i):
                        print('failed %s + %s for n=%r, found %r' % (
                            case, order, n, i))
                        sys.exit(1)
#                    traversal = list(tree.traverse())
#                    if len(traversal) != 0:
#                        print('failed %s + %s for n=%r, traversal %r' % (
#                            case, order, n, traversal))
#                        sys.exit(1)
            else:
                print("unknown case %r?" % case)
                sys.exit(1)

            w.writerow([case, order, n,
                max_iters, avg_iters,
                max_iters2, avg_iters2,
                height])
            f.flush()

if __name__ == "__main__":
    import sys
    main(*sys.argv[1:])
