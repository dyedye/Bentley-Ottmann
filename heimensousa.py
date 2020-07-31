from AvlTree import AvlBiTree
from LineSegment import LineSegment, get_intersection
import heapq


class Comparator:
    def __init__(self, y):
        # 走査線の位置
        self.y = y

    def set_y(self, y):
        self.y = y

    def __call__(self, l1):
        a1, b1, c1 = l1.coeffs
        # 線分が水平な場合は左の端点を走査線との交点とする
        if a1 == 0:
            x1 = min(l1.p1, l1.p2)[0]
        else:
            x1 = -(c1 + b1*self.y)/a1
        return x1


def push_intersection_event(line1, line2, event):
    # line1とline2が交差しているときに、その交点をeventに追加する関数
    intersection = get_intersection(line1, line2)
    if intersection is not None:
        # 交差する場合は交点イベントを追加
        left, right = min(line1, line2), max(line1, line2)
        intersect_event = - \
            intersection[1], intersection[0], intersection[1], 'intersection', [
                left, right]
        heapq.heappush(event, intersect_event)


# 線分の端点のうち、y座標が大きいものを始点、小さいものを終点イベントとして追加
comparator = Comparator(y=None)
status = AvlBiTree()
lines = []

lines.append(LineSegment((0, 0), (1, 1), comparator=comparator))
lines.append(LineSegment((-1.5, 2.5), (2.5, -1.5), comparator=comparator))
lines.append(LineSegment((-1.5, -3.5), (11.5, 9.5), comparator=comparator))

event = []
for line in lines:
    start, end = sorted([line.p1, line.p2], key=lambda x: x[1], reverse=True)
    # Max heapをheapqモジュールで実現するために、y座標にマイナスをかけた値が先頭
    start_event = -start[1], start[0], start[1], 'start', [line]
    end_event = -end[1], end[0], end[1], 'end', [line]
    heapq.heappush(event, start_event)
    heapq.heappush(event, end_event)


result = []  # 交点を格納したリスト
delta = 0.001
while len(event) > 0:
    e = heapq.heappop(event)
    e_x, e_y, event_type, line = e[1::]

    if event_type == 'start':  # 始点イベント
        line = line[0]
        comparator.set_y(e_y)  # 走査線を動かす
        status.insert(line)
        inserted_node = status.lookup(line)  # 挿入された場所のノードを取得
        right_line = status.search_higher(inserted_node.key)
        left_line = status.search_lower(inserted_node.key)

        for rl_line in [right_line, left_line]:
            if rl_line is not None:
                push_intersection_event(line, rl_line, event)

    elif event_type == 'end':  # 終点イベント
        line = line[0]
        print(f'Line End: {line}')
        removed_line = status.lookup(line).key
        right = status.search_higher(removed_line)
        left = status.search_lower(removed_line)

        if right is not None and left is not None:
            push_intersection_event(right, left, event)

        status.remove(line)
        comparator.set_y(e_y)

    elif event_type == 'intersection':  # 交点イベント
        left, right = line
        left_to_left = status.search_lower(left)
        right_to_right = status.search_higher(right)
        result.append((e_x, e_y))
        status.remove(left)
        status.remove(right)

        comparator.set_y(e_y)
        if left <= right:
            # 　線分の左右が入れ替わらなかった場合は、走査線を少し下げて、左右を入れ替える
            comparator.set_y(e_y + delta)
        status.insert(left)
        status.insert(right)

        if left_to_left is not None:
            push_intersection_event(left_to_left, right, event)
        if right_to_right is not None:
            push_intersection_event(right_to_right, left, event)
print(result)
