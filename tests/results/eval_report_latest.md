# BizTrip Copilot Evaluation Report

- 生成时间: 2026-09-06 20:36:28
- 评测模式: rag
- Query 总数: 30
- 实际执行: 15
- 通过: 15
- 失败: 0
- 跳过: 15
- 通过率: 100.0%
- 平均耗时: 0.016s
- 最大耗时: 0.035s

## 分类统计

| 分类 | 总数 | 执行 | 通过 | 失败 | 跳过 |
|------|------|------|------|------|------|
| information | 3 | 0 | 0 | 0 | 3 |
| itinerary | 5 | 0 | 0 | 0 | 5 |
| memory | 3 | 0 | 0 | 0 | 3 |
| preference | 4 | 0 | 0 | 0 | 4 |
| rag | 15 | 15 | 15 | 0 | 0 |

## 明细

| ID | Query | 预期意图 | 状态 | 耗时 | 命中关键词 / 识别意图 | Top 结果 |
|----|-------|----------|------|------|----------------------|----------|
| rag_001 | 北京出差住宿标准是多少？ | rag_knowledge | pass | 0.035s | 住宿, 标准, 北京 | 不同城市差旅注意事项 (Part 1)<br>阿里商旅差旅标准和规定 (Part 2)<br>商旅常见问题解答（FAQ） (Part 6) |
| rag_002 | 如何报销差旅费用？需要哪些材料？ | rag_knowledge | pass | 0.018s | 报销, 材料, 发票 | 商旅常见问题解答（FAQ） (Part 4)<br>商旅常见问题解答（FAQ） (Part 5)<br>差旅费用报销规定 (Part 4) |
| rag_003 | 机票应该提前多久预订比较合适？ | rag_knowledge | pass | 0.016s | 机票, 提前, 预订 | 商旅预订指南 (Part 1)<br>商旅预订指南 (Part 2)<br>商旅预订指南 (Part 3) |
| rag_004 | 航班延误了应该怎么办？ | rag_knowledge | pass | 0.015s | 航班, 延误, 改签 | 紧急情况处理指南 (Part 1)<br>紧急情况处理指南 (Part 2)<br>紧急情况处理指南 (Part 3) |
| rag_005 | 航班取消后可以改签吗？ | rag_knowledge | pass | 0.015s | 航班, 取消, 改签 | 紧急情况处理指南 (Part 2)<br>紧急情况处理指南 (Part 1)<br>商旅预订指南 (Part 1) |
| rag_006 | 出差可以携带家属吗？ | rag_knowledge | pass | 0.014s | 家属, 出差 | 商旅常见问题解答（FAQ） (Part 5)<br>商旅常见问题解答（FAQ） (Part 4)<br>紧急情况处理指南 (Part 8) |
| rag_007 | 打车费报销有什么要求？ | rag_knowledge | pass | 0.014s | 打车, 报销, 发票 | 差旅费用报销规定 (Part 4)<br>商旅常见问题解答（FAQ） (Part 4)<br>商旅常见问题解答（FAQ） (Part 2) |
| rag_008 | 酒店发票丢了还能报销吗？ | rag_knowledge | pass | 0.015s | 发票, 报销 | 差旅费用报销规定 (Part 5)<br>差旅费用报销规定 (Part 2)<br>商旅常见问题解答（FAQ） (Part 4) |
| rag_009 | 阿里商旅平台有哪些功能？ | rag_knowledge | pass | 0.015s | 平台, 申请, 预订 | 阿里商旅平台使用指南 (Part 1)<br>阿里商旅平台使用指南 (Part 10)<br>阿里商旅平台使用指南 (Part 8) |
| rag_010 | 北京有哪些常用机场？ | rag_knowledge | pass | 0.014s | 北京, 机场, 首都 | 不同城市差旅注意事项 (Part 1)<br>不同城市差旅注意事项 (Part 2)<br>不同城市差旅注意事项 (Part 7) |
| rag_011 | 上海出差有什么城市注意事项？ | rag_knowledge | pass | 0.015s | 上海, 出差, 注意 | 不同城市差旅注意事项 (Part 2)<br>不同城市差旅注意事项 (Part 3)<br>不同城市差旅注意事项 (Part 1) |
| rag_012 | 差旅途中遇到紧急情况联系谁？ | rag_knowledge | pass | 0.014s | 紧急, 联系, 情况 | 紧急情况处理指南 (Part 1)<br>紧急情况处理指南 (Part 10)<br>紧急情况处理指南 (Part 3) |
| rag_013 | 出差怎么做到环保？ | rag_knowledge | pass | 0.014s | 环保, 出差, 公共交通 | 绿色出差环保倡议 (Part 10)<br>绿色出差环保倡议 (Part 9)<br>绿色出差环保倡议 (Part 7) |
| rag_014 | 高铁和飞机预订有什么建议？ | rag_knowledge | pass | 0.013s | 高铁, 预订 | 商旅预订指南 (Part 1)<br>阿里商旅平台使用指南 (Part 6)<br>紧急情况处理指南 (Part 2) |
| rag_015 | 差旅申请审批流程是什么？ | rag_knowledge | pass | 0.017s | 差旅, 申请, 审批 | 阿里商旅差旅标准和规定 (Part 1)<br>阿里商旅差旅标准和规定 (Part 4)<br>商旅常见问题解答（FAQ） (Part 1) |
| trip_001 | 我从北京去杭州出差一周，帮我规划行程 | itinerary_planning | skipped | - | 默认离线模式只评测 RAG 检索；完整意图识别请使用 --mode full。 |  |
| trip_002 | 下周一从上海出发去深圳，周五回来，帮我安排行程 | itinerary_planning | skipped | - | 默认离线模式只评测 RAG 检索；完整意图识别请使用 --mode full。 |  |
| trip_003 | 我要去成都出差3天，安排一下住宿和交通 | itinerary_planning | skipped | - | 默认离线模式只评测 RAG 检索；完整意图识别请使用 --mode full。 |  |
| trip_004 | 2月27日从广州到北京参加会议，帮我规划路线 | itinerary_planning | skipped | - | 默认离线模式只评测 RAG 检索；完整意图识别请使用 --mode full。 |  |
| trip_005 | 我想在杭州玩两天，帮我做一个日程 | itinerary_planning | skipped | - | 默认离线模式只评测 RAG 检索；完整意图识别请使用 --mode full。 |  |
| pref_001 | 我喜欢住汉庭酒店，以后帮我记住 | preference | skipped | - | 默认离线模式只评测 RAG 检索；完整意图识别请使用 --mode full。 |  |
| pref_002 | 我还喜欢住如家 | preference | skipped | - | 默认离线模式只评测 RAG 检索；完整意图识别请使用 --mode full。 |  |
| pref_003 | 我常坐东航，座位要靠窗 | preference | skipped | - | 默认离线模式只评测 RAG 检索；完整意图识别请使用 --mode full。 |  |
| pref_004 | 我搬家到上海浦东了 | preference | skipped | - | 默认离线模式只评测 RAG 检索；完整意图识别请使用 --mode full。 |  |
| memory_001 | 我之前说过什么酒店偏好？ | memory_query | skipped | - | 默认离线模式只评测 RAG 检索；完整意图识别请使用 --mode full。 |  |
| memory_002 | 我最近去过哪些地方？ | memory_query | skipped | - | 默认离线模式只评测 RAG 检索；完整意图识别请使用 --mode full。 |  |
| memory_003 | 我上次去北京是什么时候？ | memory_query | skipped | - | 默认离线模式只评测 RAG 检索；完整意图识别请使用 --mode full。 |  |
| info_001 | 杭州下周天气怎么样？ | information_query | skipped | - | 默认离线模式只评测 RAG 检索；完整意图识别请使用 --mode full。 |  |
| info_002 | 查一下北京明天会不会下雨 | information_query | skipped | - | 默认离线模式只评测 RAG 检索；完整意图识别请使用 --mode full。 |  |
| info_003 | 搜索一下深圳最近的展会信息 | information_query | skipped | - | 默认离线模式只评测 RAG 检索；完整意图识别请使用 --mode full。 |  |

## 说明

默认 RAG 模式只评测本地知识库检索链路，不调用外部 LLM。非 RAG Query 会被记录为 skipped；配置 API key 后可使用 `python tests/run_eval.py --mode full` 评测意图识别。
