# 全台週邊美食清單：「不感興趣」回饋

網頁上每個景點與每家餐廳都有「不感興趣」勾選框（存在瀏覽器 localStorage，key `tfg_notint`）。左下角按鈕會開一張預填好的 GitHub issue（標籤 `not-important`）到 1234yyyyyy/taiwan-food-guide，列出 城市／景點／餐廳。

## 每次推薦或更新前（必做，最先執行）
```bash
cd /workspace/taiwan-food-site && python3 feedback.py
```
- 產生／更新 `not_interested.json`（type: attraction|restaurant, city, attraction, name, desc, category_hints, issue, date）。
- 之後的推薦、新增景點或餐廳，凡與清單中項目**同主題／同類型**（同一景點、同類景點如夜市／老街／寺廟、同類餐廳如同種料理或同類小吃）一律排除；拿不準時偏向排除。
- 每份報告都要寫一行：「本次因不感興趣回饋排除 X 則」。
- 處理完關閉 issue：`gh issue close <N> -R 1234yyyyyy/taiwan-food-guide -c "已收到，YYYY-MM-DD 起排除同類內容（共 X 則）"`。
