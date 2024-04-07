import re

def encapsulate_sql(lines: list) -> str:
    content = ''.join(lines)

    patterns = [
        r"drop\s+table.*?;.*?create\s+table.*?;",
        r"delete\s+from.*?where.*?;.*?insert\s+into.*?;",
        r"(drop\s+table[^;]*?;(\s*drop\s+table[^;]*?;)*)",
        r"(analyze\s+.*?;\s*)+",
        #r"analyze\s+.*;",
        r"(.*?;)"
    ]
    
    matches = []
    
    # 步骤1: 按顺序遍历每个模式，对内容执行搜索
    for pattern in patterns:
        for match in re.finditer(pattern, content, re.I | re.S):
            # 步骤2: 检查是否与之前的匹配有重叠
            overlap = any(existing_match.start() < match.end() and existing_match.end() > match.start() for existing_match in matches)
            if not overlap:
                matches.append(match)

    # 步骤3: 根据所有非重叠匹配的开始位置进行排序
    matches.sort(key=lambda x: x.start())

    all_blocks = []
    result = []
    last_end = 0

    # 步骤4: 逐个处理每个匹配，替换为占位符并存储匹配的块
    for match in matches:
        start, end = match.span()
        result.append(content[last_end:start])
        block = match.group()
        all_blocks.append(block)
        
        # 打印输出的内容块
        print("Matched Block:")
        print("------------------")
        print(block)
        print("------------------\n")
        
        placeholder = f"PLACEHOLDER_FOR_BLOCK{len(all_blocks)}"
        result.append(placeholder)
        
        last_end = end
    
    result.append(content[last_end:])  # 添加剩余部分

    def encapsulate_block(block):
        return (f"\nv_start_time := clock_timestamp();\n"
                f"vc_sql:='\n"
                f"{block}\n"
                f"'\n;\n"
                f"RAISE notice 'step:%', vc_sql;\n"
                f"execute vc_sql;\n"
                f"v_end_time := clock_timestamp();\n"
                f"RAISE NOTICE '耗时: %', (v_end_time - v_start_time);\n")

    # 步骤5: 使用占位符构建最终输出
    output = ''.join(result)
    for index, block in enumerate(all_blocks, start=1):
        encapsulated_block = encapsulate_block(block)
        placeholder = f"PLACEHOLDER_FOR_BLOCK{index}"
        output = output.replace(placeholder, encapsulated_block, 1)

    return output
