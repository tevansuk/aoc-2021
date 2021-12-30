from dataclasses import dataclass, field
from typing import Optional

Room = tuple[int, ...]  # type: ignore
COSTS = [0, 1, 10, 100, 1000]
DOORS = [-1, 2, 4, 6, 8]
ABCD = " ABCD"


@dataclass(frozen=True)
class Move:
    piece: int
    froom: int
    fidx: int
    troom: int
    tidx: int

    def cost(self):
        if self.froom == 0:
            moves = abs(DOORS[self.piece] - self.fidx) + self.tidx + 1
        elif self.troom == 0:
            moves = abs(DOORS[self.froom] - self.tidx) + self.fidx + 1
        else:
            moves = 2 + self.fidx + abs(DOORS[self.piece] - DOORS[self.froom]) + self.tidx
        return moves * COSTS[self.piece]


def hallway_clear(hallway: Room, ppos: int, dpos: int) -> bool:
    ppos = ppos - 1 if ppos > dpos else ppos + 1
    pos, pos2 = sorted((ppos, dpos))
    return all((h == 0 for h in hallway[pos : pos2 + 1]))


def room_has_space(room: Room, piece: int) -> int:
    if all(pos in (piece, 0) for pos in room):
        return sum(1 for pos in room if pos == 0) - 1
    return -1


@dataclass(frozen=True)
class Board:
    # The hallway is room 0
    rooms: tuple[Room, ...]
    move: Optional[Move] = field(compare=False, default=None)

    def apply(self, move: Move) -> "Board":
        rooms: list[list[int]] = list(list(room) for room in self.rooms)
        rooms[move.froom][move.fidx] = 0
        rooms[move.troom][move.tidx] = move.piece
        return self.__class__(rooms=tuple(tuple(room) for room in rooms), move=move)

    def moves(self) -> list[Move]:
        moves = self.hallway_to_room_moves()
        if moves:
            return moves
        moves = self.room_to_room_moves()
        if moves:
            return moves
        return self.room_to_hallway_moves()

    def hallway_to_room_moves(self) -> list[Move]:
        moves = []
        # Can a hallway piece move to its room
        for idx, h in enumerate(self.rooms[0]):
            if h > 0:
                if not hallway_clear(self.rooms[0], idx, DOORS[h]):
                    continue
                # Can move if room is empty or has all the right type
                if (ridx := room_has_space(self.rooms[h], h)) != -1:
                    moves.append(Move(h, 0, idx, h, ridx))
        return moves

    def room_to_room_moves(self) -> list[Move]:
        moves = []
        # Can a room piece move directly to its proper room
        for ridx, room in enumerate(self.rooms):
            # Skip the hallway
            if ridx == 0:
                continue
            # is the room empty
            top = next((r for r in enumerate(room) if r[1] != 0), None)
            if top is None:
                continue
            idx, piece = top
            # Does it want to move to another room directly
            if piece == ridx:
                continue
            # Is there anything between this room and that room
            if not hallway_clear(self.rooms[0], DOORS[ridx], DOORS[piece]):
                continue
            if (tridx := room_has_space(self.rooms[piece], piece)) != -1:
                moves.append(Move(piece, ridx, idx, piece, tridx))
        return moves

    def room_to_hallway_moves(self) -> list[Move]:
        moves = []
        # Can a room piece move to the hallway
        for ridx, room in enumerate(self.rooms):
            # Skip the hallway
            if ridx == 0:
                continue
            # is the room empty
            top = next((r for r in enumerate(room) if r[1] != 0), None)
            if top is None:
                continue
            idx, piece = top
            # Can move to any hallway space thats not a door not occupied by a piece
            # if nothing is blocking it
            # Going left
            for direction in (range(DOORS[ridx], -1, -1), range(DOORS[ridx], len(self.rooms[0]))):
                for hidx in direction:
                    if hidx in DOORS:
                        continue
                    if self.rooms[0][hidx] != 0:
                        break
                    moves.append(Move(piece, ridx, idx, 0, hidx))
        return moves

    def __str__(self) -> str:
        return "\n".join(
            (
                f"┏{'━' * 11}┓",
                f"┃{''.join(ABCD[v] for v in self.rooms[0])}┃",
                f"┗━┓{'┃'.join(ABCD[r[0]] for r in self.rooms[1:])}┏━┛",
                *(
                    f"  ┃{'┃'.join(ABCD[r[idx]] for r in self.rooms[1:])}┃"
                    for idx in range(1, len(self.rooms[1]))
                ),
                f"  ┗{'━' * 7}┛",
            )
        )

    @classmethod
    def parse(cls, lines: list[str]) -> "Board":
        _, hallway_, *rooms_ = lines
        hallway = tuple(0 for c in hallway_ if c == ".")
        rooms__ = [[ABCD.index(c) for c in r.lstrip() if c in ABCD] for r in rooms_[:-1]]
        return cls(rooms=(hallway, *tuple(zip(*rooms__))))
