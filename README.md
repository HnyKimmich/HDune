```text
    project_root/
    ├── main.py                          # 程序入口，初始化依赖注入和主窗口
    ├── requirements.txt                 # 依赖列表（如 PyQt5, dataclasses, typing_extensions）
    │
    ├── data/                         # 配置文件目录
    │   ├── cards/                       # 卡牌数据（JSON）
    │   │   ├── imperial_cards.json       # 帝国牌堆定义
    │   │   ├── initial_cards.json       # 帝国牌堆定义
    │   │   ├── conflict_cards.json       # 冲突牌堆定义
    │   │   ├── intrigue_cards.json       # 阴谋牌堆定义
    │   │   ├── reserch_cards.json       # 二扩牌堆定义
    │   │   ├── shared_cards.json       # 公共牌堆定义
    │   └── maps/
    │       └── default_map.json         # 地图区域定义
    │   └── leaders/
    │       └── leaders.json         # 领袖定义
    │
    ├── common/                          # 通用基础组件
    │   ├── __init__.py
    │   ├── observable.py                # Observable 基类（INotifyPropertyChanged）
    │   ├── relay_command.py             # RelayCommand 实现
    │   ├── interfaces.py                # 核心接口（Protocol / ABC）
    │   ├── event_bus.py                 # 事件总线（可选）
    │   ├── dependency_injection.py      # 简单的依赖注入容器
    │   └── utilities/
    │       ├── json_loader.py
    │       ├── async_image_loader.py    # 异步图片加载器
    │       ├── object_pool.py
    │       └── hex_grid_calc.py
    │
    ├── model/                           # 业务模型（无 GUI 依赖）
    │   ├── __init__.py
    │   ├── card/                        # 卡牌模块
    │   │   ├── __init__.py
    │   │   ├── card.py                  # 卡牌数据类（id, name, cost, effect_type...）
    │   │   ├── card_library.py          # 卡牌库（所有卡牌静态数据）
    │   │   ├── deck_controller.py       # 牌堆控制器（管理卡牌序列、抽牌）
    │   │   └── effect/                  # 效果子系统
    │   │       ├── __init__.py
    │   │       ├── base.py              # IEffect 接口
    │   │       ├── composite.py         # 组合效果（串联执行）
    │   │       ├── concrete/            # 具体效果实现
    │   │       │   ├── gain_resource.py
    │   │       │   ├── draw_card.py
    │   │       │   ├── move_agent.py
    │   │       │   └── trigger_conflict.py
    │   │       └── factory.py           # 效果工厂
    │   ├── map/                         # 地图模块
    │   │   ├── __init__.py
    │   │   ├── region.py                # 区域数据类（id, type, position, special_rules）
    │   │   ├── map_controller.py        # 地图核心逻辑（区域管理、移动规则、特使位置）
    │   │   └── map_data_loader.py       # 地图数据加载器
    │   ├── player/                      # 玩家模块
    │   │   ├── __init__.py
    │   │   ├── player.py                # 玩家数据类（id, name, resources, hand_cards...）
    │   │   ├── player_manager.py        # 玩家管理器（4个玩家实例，回合顺序）
    │   │   └── resource_types.py        # 资源类型枚举
    │   └── game/                        # 游戏整体规则
    │       ├── __init__.py
    │       ├── turn_controller.py       # 回合与阶段管理
    │       ├── conflict_controller.py   # 冲突（战斗）逻辑
    │       ├── game_rule_service.py     # 胜利条件、全局规则
    │       └── action_log.py            # 操作历史记录
    │
    ├── viewmodel/                       # 视图模型（UI 状态与交互逻辑，无 GUI 框架依赖）
    │   ├── __init__.py
    │   ├── map/
    │   │   ├── __init__.py
    │   │   ├── map_viewmodel.py         # 地图总 ViewModel（区域集合、选中状态）
    │   │   └── region_viewmodel.py      # 单个区域 ViewModel（是否可选、高亮）
    │   ├── card/
    │   │   ├── __init__.py
    │   │   ├── card_viewmodel.py        # 单张卡牌 ViewModel（名称、费用、图片异步加载）
    │   │   ├── hand_viewmodel.py        # 手牌面板 ViewModel（卡牌列表、出牌命令）
    │   │   ├── deck_viewmodel.py        # 公共牌堆 ViewModel（顶部卡牌、剩余数量）
    │   │   ├── discard_pile_viewmodel.py# 弃牌堆 ViewModel
    │   │   └── card_detail_viewmodel.py # 卡牌详情弹窗 ViewModel
    │   ├── player/
    │   │   ├── __init__.py
    │   │   └── player_info_viewmodel.py # 单个玩家信息面板 ViewModel（资源、领袖、分数）
    │   ├── game/
    │   │   ├── __init__.py
    │   │   ├── game_hud_viewmodel.py    # 顶部 HUD（回合数、当前阶段、当前玩家）
    │   │   ├── conflict_viewmodel.py    # 冲突区 ViewModel（奖励卡、参与情况）
    │   │   ├── action_log_viewmodel.py  # 操作历史 ViewModel
    │   │   └── game_summary_viewmodel.py# 游戏结束统计 ViewModel
    │   ├── settings/
    │   │   ├── __init__.py
    │   │   └── settings_viewmodel.py    # 设置菜单 ViewModel
    │   └── common/
    │       ├── __init__.py
    │       └── dialog_viewmodel.py      # 通用弹窗 ViewModel（确认框等）
    │
    ├── view/                            # 视图（GUI 实现，以 PyQt5 为例）
    │   ├── __init__.py
    │   ├── main_window.py               # 主窗口，管理各视图布局
    │   ├── map/
    │   │   ├── __init__.py
    │   │   ├── map_view.py              # 地图视图（容器，管理 RegionView 对象池）
    │   │   ├── region_view.py           # 单个区域视图（显示背景、图标，响应点击）
    │   │   └── region_pool.py           # Region 视图对象池
    │   ├── card/
    │   │   ├── __init__.py
    │   │   ├── card_view.py             # 卡牌视图（显示图片、名称、费用）
    │   │   ├── hand_view.py             # 手牌面板视图（横向/弧形布局）
    │   │   ├── deck_view.py             # 公共牌堆视图
    │   │   ├── discard_pile_view.py
    │   │   └── card_detail_dialog.py    # 卡牌详情弹窗
    │   ├── player/
    │   │   ├── __init__.py
    │   │   └── player_info_panel.py     # 单个玩家信息面板（资源条、头像）
    │   ├── game/
    │   │   ├── __init__.py
    │   │   ├── game_hud.py              # 顶部 HUD 控件
    │   │   ├── conflict_area.py         # 冲突区控件（展示奖励卡、冲突标记）
    │   │   ├── action_log_widget.py     # 历史记录列表
    │   │   └── game_summary_dialog.py   # 游戏结束弹窗
    │   ├── settings/
    │   │   ├── __init__.py
    │   │   └── settings_dialog.py       # 设置弹窗
    │   └── common/
    │       ├── __init__.py
    │       ├── command_button.py        # 绑定 ICommand 的按钮封装
    │       └── loading_overlay.py       # 加载动画控件
    │
    ├── services/                        # 服务层（依赖注入、启动、资源管理）
    │   ├── __init__.py
    │   ├── bootstrapper.py              # 启动器：初始化所有 Model、ViewModel，注入依赖
    │   ├── resource_manager.py          # 资源管理器（图片加载与缓存）
    │   └── scene_manager.py             # 场景切换（如主菜单→游戏界面）
    │
    └── assets/                          # 资源文件（图片、音频、字体等）
        ├── images/
        │   ├── cards/                   # 卡牌图片（缩略图、大图）
        │   ├── map/                     # 地图背景、区域图标
        │   ├── ui/                      # UI 控件图片（按钮、面板边框）
        │   └── avatars/                 # 玩家头像
```