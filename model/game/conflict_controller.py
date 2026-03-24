import json
from pathlib import Path
from typing import List, Dict, Optional
from .conflict_card import ConflictCard

class ConflictController:
    def __init__(self):
        self.conflict_deck: List[ConflictCard] = []
        self.current_conflict: Optional[ConflictCard] = None

    def load_conflict_deck(self, file_path: Path):
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.conflict_deck = [ConflictCard.from_dict(item) for item in data]

    def draw_conflict_card(self) -> ConflictCard:
        if not self.conflict_deck:
            raise ValueError("No conflict cards left")
        self.current_conflict = self.conflict_deck.pop()
        return self.current_conflict

    def resolve_conflict(self, player_powers: Dict[int, int]) -> Dict[int, List[str]]:
        """
        根据玩家力量值分配奖励。
        player_powers: {player_id: power}
        返回 {player_id: [奖励描述]}，并列时都取更低级奖励。
        """
        sorted_players = sorted(player_powers.items(), key=lambda x: x[1], reverse=True)
        rewards = []
        for i, (pid, power) in enumerate(sorted_players):
            # 找到并列的玩家范围
            if i > 0 and power == sorted_players[i-1][1]:
                # 并列，奖励与前一玩家相同（更低级）
                rank = i  # 从0开始，实际排名+1
            else:
                rank = i + 1
            # 从冲突卡中获取对应排名的奖励
            if rank <= len(self.current_conflict.rewards):
                reward = self.current_conflict.rewards[rank-1]
                rewards.append((pid, reward))
            else:
                rewards.append((pid, None))
        # 整理返回格式
        result = {}
        for pid, reward in rewards:
            result[pid] = reward if reward else []
        return result