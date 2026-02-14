import re
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, ConnectionPatch
import numpy as np
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="matplotlib")
# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
# ======== 解析 interaction.txt 文件 ========
def parse_interaction_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Players
    players_block = re.search(r'Players(.*?)AND Interactions', content, re.S).group(1)
    players = {}
    for line in players_block.splitlines():
        m = re.match(r'\s*Player\s+([A-Z]):\s*(.+)', line)
        if m:
            players[m.group(1)] = m.group(2).strip()

    # AND Interactions
    and_block = re.search(r'AND Interactions(.*?)OR Interactions', content, re.S).group(1)
    and_inter = {}
    for line in and_block.splitlines():
        m = re.match(r'I\((.*?)\):\s*([-0-9.]+)', line)
        if m:
            and_inter[m.group(1)] = float(m.group(2))

    # OR Interactions
    or_block = re.search(r'OR Interactions(.*)', content, re.S).group(1)
    or_inter = {}
    for line in or_block.splitlines():
        m = re.match(r'I\((.*?)\):\s*([-0-9.]+)', line)
        if m:
            or_inter[m.group(1)] = float(m.group(2))

    return players, and_inter, or_inter

# ======== 使用matplotlib绘制层次化树 ========
def draw_custom_tree(players, and_inter, or_inter, output="interaction_tree", num_columns=4, items_per_column=4):
    """
    绘制交互树
    
    参数:
        players: 玩家字典
        and_inter: AND交互字典
        or_inter: OR交互字典
        output: 输出文件名
        num_columns: 主干线列数，支持2-6列，默认4列
        items_per_column: 每列的节点数量，默认4个
    """
    # 创建图形和轴
    fig, ax = plt.subplots(1, 1, figsize=(16, 12))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # 确保列数在合理范围内
    num_columns = max(2, min(6, num_columns))
    # 确保每列节点数量在合理范围内（1-10个）
    items_per_column = max(1, min(10, items_per_column))
    
    # 根据列数和每列节点数动态计算需要取多少个交互
    # 多取一些作为缓冲以防溢出后移动
    items_needed = num_columns * items_per_column + 10  # 多取10个作为缓冲
    
    # 取足够数量的 AND、OR 交互（按 I 的绝对值大小排序）
    top_and = sorted(and_inter.items(), key=lambda x: -abs(x[1]))[:items_needed]
    top_or = sorted(or_inter.items(), key=lambda x: -abs(x[1]))[:items_needed]

    # 颜色映射（根据 I 值深浅变色）
    def hex_to_rgb(hex_str):
        hex_str = hex_str.lstrip('#')
        return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))

    def rgb_to_hex(rgb_tuple):
        return '#%02x%02x%02x' % rgb_tuple

    def lerp(a, b, t):
        return int(round(a + (b - a) * t))

    def lerp_color(c1_hex, c2_hex, t):
        r1, g1, b1 = hex_to_rgb(c1_hex)
        r2, g2, b2 = hex_to_rgb(c2_hex)
        r = lerp(r1, r2, t)
        g = lerp(g1, g2, t)
        b = lerp(b1, b2, t)
        return rgb_to_hex((r, g, b))

    # 计算实际绘制节点的 I 值绝对值范围，用于归一化（确保透明度从0到1）
    all_vals = [v for _, v in top_and] + [v for _, v in top_or]
    all_abs_vals = [abs(v) for v in all_vals]
    if len(all_abs_vals) > 0:
        min_abs_I = min(all_abs_vals)
        max_abs_I = max(all_abs_vals)
    else:
        min_abs_I = 0.0
        max_abs_I = 1.0
    
    # 避免除零
    if max_abs_I == min_abs_I:
        max_abs_I = min_abs_I + 1e-6

    # 根节点位置
    root_x, root_y = 5.0, 8
    ax.add_patch(plt.Circle((root_x, root_y), 0.2, color='lightgrey', zorder=3))
    ax.text(root_x, root_y, '+', ha='center', va='center', fontsize=36, fontweight='bold', zorder=4)

    # 将AND和OR交互合并，按I值绝对值排序后分配
    all_interactions = top_and + top_or
    all_interactions = sorted(all_interactions, key=lambda x: -abs(x[1]))
    
    # 动态生成列数据 - 初始分配
    columns = []
    for i in range(num_columns):
        start_idx = i * items_per_column
        end_idx = start_idx + items_per_column
        columns.append(list(all_interactions[start_idx:end_idx]))
    
    # 根据列数动态计算列位置和max_line_len
    # 原则：确保最右侧列不超过x=7.8，为特征单词预留空间
    # 同时根据列数调整max_line_len，防止列间重叠
    max_trunk_x = 7.8
    
    if num_columns == 2:
        col_x_positions = [2.0, 7.1]
        max_line_len = 3.0
    elif num_columns == 3:
        col_x_positions = [1.0, 4.2, 7.1]
        max_line_len = 2.6
    elif num_columns == 4:
        col_x_positions = [0.5, 2.8, 5.5, 7.8]
        max_line_len = 2.2
    elif num_columns == 5:
        col_x_positions = [0.5, 2.3, 4.2, 6.0, 7.8]
        max_line_len = 1.6
    else:  # 6列
        col_x_positions = [0.3, 1.8, 3.3, 4.8, 6.3, 7.8]
        max_line_len = 1.3
    
    colors = ["#155fa0"] * num_columns  # 全部蓝色
    
    print(f"  [INFO] number of columns: {num_columns}, nodes each column: {items_per_column}, max_line_len: {max_line_len}")
    print(f"  [INFO] number of interactions: {len(all_interactions)}, Initial distribution: {num_columns} column × {items_per_column} nodes = {num_columns * items_per_column}")
    
    # 创建每列
    for col_idx, col_data in enumerate(columns):
        if len(col_data) == 0:
            continue
            
        # 不再固定AND/OR类型，每个节点根据具体数据判断
        logic_type = "MIXED"  # 混合类型
        col_x = col_x_positions[col_idx]
        color = colors[col_idx]
        
        # 主干线从根节点到列顶
        trunk_y_start = root_y
        trunk_y_end = 7.5
        
        # 绘制主干线
        ax.plot([root_x, col_x], [trunk_y_start, trunk_y_end], 
                color=color, linewidth=4, zorder=1)
        
        # 删除列标题
        
        # 创建列中的节点 - 水平排列函数和特征，文本框紧贴内容
        start_y = 6.8
        cursor_y = start_y
        line_gap = 0.55  # 固定的节点间距
        
        for depth, (key, val) in enumerate(col_data):
            words = [players.get(ch, ch) for ch in key]
            node_y = cursor_y
            
            # 精确计算该节点的实际高度，用于边界检查
            # 先模拟分行以获得准确的行数
            temp_word_width_map = [max(0.45, 0.055 * len(w) + 0.25) for w in words]
            temp_lines = []
            temp_line = []
            temp_len = 0.0
            gap_h = 0.06
            for w, w_width in zip(words, temp_word_width_map):
                if not temp_line:
                    temp_line = [w]
                    temp_len = w_width
                else:
                    projected = temp_len + gap_h + w_width
                    if projected <= max_line_len:
                        temp_line.append(w)
                        temp_len = projected
                    else:
                        temp_lines.append(temp_line)
                        temp_line = [w]
                        temp_len = w_width
            if temp_line:
                temp_lines.append(temp_line)
            
            num_lines = len(temp_lines) if temp_lines else 0
            box_h = 0.28
            gap_v = 0.10
            actual_box_area_height = num_lines * box_h + max(0, num_lines - 1) * gap_v
            beam_and_formula_height = 0.2 + 0.16  # 横梁 + 公式文本
            total_node_height = actual_box_area_height + beam_and_formula_height
            
            # 检查节点底部是否会超出边界
            predicted_bottom = node_y - total_node_height
            if predicted_bottom < 0.4:  # 底部安全边界
                # 将当前节点及后续节点移到下一列
                remaining_nodes = col_data[depth:]
                
                if col_idx + 1 < len(columns):
                    # 将剩余节点添加到下一列的开头
                    columns[col_idx + 1] = list(remaining_nodes) + columns[col_idx + 1]
                    print(f"  [INFO] Starting from columne {col_idx} node {depth}, in total {len(remaining_nodes)} exceed the boundary，moved to column {col_idx+1}")
                else:
                    print(f"  [WARNING] starting from column {col_idx} node {depth} in total {len(remaining_nodes)} nodes exceed the boundary，but it is the last column，cant plot")
                break
            
            # ---- 以"挂词"形式绘制特征组：若干小方框 + 顶部横梁 + 与主干的连线 ----
            def draw_word_group(ax, base_x, center_y, word_list):
                if not word_list:
                    return {'total_height': 0, 'box_height': 0, 'bottom_y': center_y}
                
                # 方框参数（与compare_all_llms.py保持一致）
                box_height = 0.28
                box_padding = 0.04
                gap_horizontal = 0.06
                gap_vertical = 0.10
                
                # 使用外层传入的max_line_len
                # 先计算每个单词对应的方框宽度
                word_width_map = [max(0.45, 0.055 * len(w) + 0.25) for w in word_list]
                lines = []
                per_line_word_widths = []
                current_line = []
                current_widths = []
                current_len = 0.0
                for w, w_width in zip(word_list, word_width_map):
                    if not current_line:
                        current_line = [w]
                        current_widths = [w_width]
                        current_len = w_width
                    else:
                        projected = current_len + gap_horizontal + w_width
                        if projected <= max_line_len:
                            current_line.append(w)
                            current_widths.append(w_width)
                            current_len = projected
                        else:
                            lines.append(current_line)
                            per_line_word_widths.append(current_widths)
                            current_line = [w]
                            current_widths = [w_width]
                            current_len = w_width
                if current_line:
                    lines.append(current_line)
                    per_line_word_widths.append(current_widths)
                
                # 计算每行宽度（用于对齐），使用已计算的每词宽度
                line_widths = []
                for widths in per_line_word_widths:
                    if len(widths) == 0:
                        line_widths.append(0)
                    elif len(widths) == 1:
                        line_widths.append(widths[0])
                    else:
                        line_widths.append(sum(widths) + gap_horizontal * (len(widths) - 1))
                
                max_line_width = max(line_widths) if line_widths else 0
                group_center_x = base_x + max_line_width/2 + 0.1
                
                # 计算整体高度
                total_height = len(lines) * box_height + (len(lines) - 1) * gap_vertical
                # 统一处理：所有节点都使用传入的center_y作为方框顶部起始位置
                start_y = center_y
                
                # 目标行宽：各行的最大宽度，使每行长度大致相同
                target_line_width = max(line_widths) if line_widths else 0

                # 绘制每一行（不足的行通过增大间距补齐，总体居中）
                current_y = start_y
                all_boxes = []  # 记录所有方框位置，用于绘制横梁
                
                for line_idx, line in enumerate(lines):
                    widths = per_line_word_widths[line_idx]
                    if len(widths) == 0:
                        current_y -= box_height + gap_vertical
                        continue
                    if len(widths) == 1:
                        actual_line_width = widths[0]
                        adaptive_gap = 0.0
                        draw_line_width = actual_line_width
                    else:
                        actual_line_width = sum(widths) + gap_horizontal * (len(widths) - 1)
                        if actual_line_width < target_line_width * 0.95:
                            adaptive_gap = gap_horizontal
                            draw_line_width = actual_line_width
                        else:
                            extra = max(0.0, target_line_width - actual_line_width)
                            adaptive_gap = gap_horizontal + (extra / (len(widths) - 1))
                            draw_line_width = target_line_width

                    line_start_x = group_center_x - draw_line_width / 2
                    current_x = line_start_x
                    
                    for idx, word in enumerate(line):
                        word_width = widths[idx]
                        
                        # 绘制方框（蓝色底，填充透明度由I值绝对值决定，边框不透明）
                        # 根据该组的 I 值的绝对值计算透明度，使用min-max归一化
                        abs_val = abs(val)
                        t = (abs_val - min_abs_I) / (max_abs_I - min_abs_I)  # 归一化到[0,1]
                        # 将RGB颜色转换为RGBA格式，只给填充色添加透明度
                        face_color_rgba = (0.498, 0.702, 0.902, t)  # #7fb3e6 转为RGBA
                        rect = FancyBboxPatch(
                            (current_x, current_y - box_height / 2),
                            word_width+0.01, box_height,
                            boxstyle="round,pad=0.02", linewidth=1.6,
                            edgecolor="#155fa0",  # 边框蓝色，不透明
                            facecolor=face_color_rgba,  # 填充色带透明度
                            zorder=2
                        )
                        
                        ax.add_patch(rect)
                        
                        # 绘制单词：根据长度自适应字号
                        font_size = 18 if len(word) < 10 else 16
                        ax.text(
                            current_x + word_width/2, current_y, word,
                            ha='center', va='center',
                            fontsize=font_size, color='black', zorder=3,
                        )
                        
                        all_boxes.append((current_x, current_y, word_width, box_height))
                        current_x += word_width + (adaptive_gap if len(widths) > 1 else 0.0)
                    
                    current_y -= box_height + gap_vertical
                
                # 绘制顶部横梁
                if all_boxes:
                    # 找到最左和最右的方框
                    leftmost_x = min(box[0] for box in all_boxes)
                    rightmost_x = max(box[0] + box[2] for box in all_boxes)
                    # 向上再加0.1个单位
                    beam_offset = 0.2
                    top_y = start_y + box_height/2 + beam_offset

                    
                    
                    # 若仅有一个单词，连接横梁末端与该方框顶部横线的中点
                    if len(all_boxes) == 1:
                        box_x, box_y, box_w, box_h = all_boxes[0]
                        box_center_x = box_x + box_w / 2.0
                        box_top_y = box_y + box_h / 2  # 方框顶部横线的y坐标
                        # 末端取横梁右端
                        ax.plot([(leftmost_x + rightmost_x) / 2, (leftmost_x + rightmost_x) / 2], [top_y, box_top_y],
                                color='gray', linewidth=1.0, zorder=1)


                        # 横梁（从主干起点到右端，避免起点超出主干）
                        ax.plot([base_x, (rightmost_x+leftmost_x)/2], [top_y, top_y], 
                            color='gray', linewidth=1.2, zorder=1)

                        

                    # 若特征单词数量大于1，则绘制方括号
                    elif len(all_boxes) > 1:
                        # 取得第一行特征单词的所有方框
                        num_first_line = len(lines[0])
                        first_line_boxes = all_boxes[:num_first_line]
                        # 起点：第一行最左侧方框的顶端横线中点
                        first_left_box = first_line_boxes[0]
                        left_top_mid_x = first_left_box[0] + first_left_box[2] / 2
                        left_top_mid_y = first_left_box[1] + first_left_box[3] / 2
                        # 终点：第一行最右侧方框的顶端横线中点
                        first_right_box = first_line_boxes[-1]
                        
                        right_top_mid_x = first_right_box[0] + first_right_box[2] / 2
                        right_top_mid_y = first_right_box[1] + first_right_box[3] / 2
                        # 根据方框坐标，顶端横线的 y 其实是 box_y + box_height/2
                        left_top_mid_y = first_left_box[1] + first_left_box[3]/2
                        right_top_mid_y = first_right_box[1] + first_right_box[3]/2
                        # 方括号高度
                        bracket_height = 0.1
                        # 方括号左上竖线
                        ax.plot([left_top_mid_x, left_top_mid_x], [left_top_mid_y, left_top_mid_y + bracket_height], color='gray', linewidth=1.3, zorder=2)
                        # 方括号右上竖线
                        ax.plot([right_top_mid_x, right_top_mid_x], [right_top_mid_y, right_top_mid_y + bracket_height], color='gray', linewidth=1.3, zorder=2)
                        # 方括号顶横线
                        ax.plot([left_top_mid_x, right_top_mid_x],
                                [left_top_mid_y + bracket_height, right_top_mid_y + bracket_height],
                                color='gray', linewidth=1.3, zorder=2)
                        # 方括号顶横线中点
                        bracket_mid_x = (left_top_mid_x + right_top_mid_x) / 2
                        bracket_top_y = (left_top_mid_y + bracket_height + right_top_mid_y + bracket_height) / 2
                        # 横梁末端
                        beam_end_x =bracket_mid_x
                        beam_end_y = top_y
                        # 用竖线将 bracket_mid_x, bracket_top_y 与 beam_end_x, beam_end_y 连接
                        ax.plot([beam_end_x, bracket_mid_x], [beam_end_y, bracket_top_y],
                                color='gray', linewidth=1.0, zorder=1, linestyle='-')


                        # 横梁（从主干起点到右端，避免起点超出主干）
                        ax.plot([base_x, bracket_mid_x], [top_y, top_y], 
                            color='gray', linewidth=1.2, zorder=1)

                    # 横梁中心
                    beam_center_x = (base_x + rightmost_x) / 2
                    ax.plot([base_x, base_x], [trunk_y_end, top_y], 
                            color="#155fa0", linewidth=2 if depth == 0 else 2, 
                            linestyle='-' if depth == 0 else '-', zorder=6)


                    

                    
                    
                    # 在特征单词组正上方添加函数值文本
                    formula_y = top_y + 0.16
                    # 根据key判断是AND还是OR交互
                    if key in and_inter and abs(val - and_inter[key]) < 1e-6:
                        formula_text = r'$I_S^{AND}=' + f'{val:.4f}$'
                    elif key in or_inter and abs(val - or_inter[key]) < 1e-6:
                        formula_text = r'$I_S^{OR}=' + f'{val:.4f}$'
                    else:
                        formula_text = r'$I_S=' + f'{val:.4f}$'
                    ax.text(base_x+0.1, formula_y, formula_text, 
                           ha='left', va='center', fontsize=15, fontweight='bold', color='black', zorder=4)
                
                # 返回节点信息，包括特征方框的底部Y坐标
                return {
                    'total_height': total_height,
                    'box_height': box_height,
                    'bottom_y': min(box[1] - box[3]/2 for box in all_boxes) if all_boxes else (center_y - 0.2)
                }

            metrics = draw_word_group(ax, col_x, node_y, words)
            
            # 计算下一个节点的位置：当前节点底部 - 固定间距
            if depth + 1 < len(col_data):
                fixed_gap = 0.8  # 固定的节点间距
                # 下一个节点的方框顶部位置 = 当前节点底部 - 固定间距
                cursor_y = metrics['bottom_y'] - fixed_gap

    # 添加图例
#    ax.text(5, 0.5, 'blue：interactions', 
#           ha='center', va='center', fontsize=12, 
#           bbox=dict(boxstyle="round,pad=0.3", facecolor='lightgray', alpha=0.8))

    plt.tight_layout()
    # 获取当前脚本所在目录
    import os
    plt.savefig(output, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"the generated PDF file is {output}")

