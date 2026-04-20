---
header: LiveCodeBench רב-שפתי
navHome: ראשי
navLeaderboard: טבלת מובילים
navCompare: השוואה
navNews: חדשות
newsTitle: עדכונים
---

**Multi-LCB** מרחיב את **LiveCodeBench (LCB)** — מדד דה‑פקטו להערכה מודעת‑זליגה (contamination‑aware) של יצירת קוד — מהקשר **של Python בלבד** למדד **רב‑שפתי**, המכסה **12 שפות תכנות** (C++, C#, Python, Java, Rust, Go, TypeScript, JavaScript, Ruby, PHP, Kotlin, Scala) תחת פרוטוקול הערכה אחיד של STDIN/STDOUT.

---

כל משימה מקורית של LiveCodeBench מומרת למשימות שקולות בכל השפות הנתמכות, תוך שמירה על **הערכה מודעת‑זליגה** (סינון לפי תאריך שחרור), **עדכונים חיים**, ואותה מטריקה של **Pass@1**. במעבר מהפורמט הפונקציונלי המקורי לממשק STDIN/STDOUT המאוחד אנו רואים רק **שינויים קטנים ב‑Pass@1**: כלומר הפורמט החדש שומר על קושי המשימות ועל דירוגי המודלים, ובמקביל מאפשר הערכה רב‑שפתית עקבית.

הערכת **24+ מודלים מודרניים** על Multi‑LCB מראה ש:
- **Python איננה פרוקסי אמין** לשפות אחרות — דירוגי מודלים יכולים להשתנות משמעותית מחוץ ל‑Python;
- מודלים רבים מציגים **התאמת‑יתר ל‑Python** — ציונים חזקים ב‑Python לצד ירידות חדות בשפות אחרות;
- קיימת **זליגה ספציפית לשפה** ופערי ביצועים גדולים בין שפות, במיוחד בשפות סטטיות ופחות נפוצות.

כתוצאה מכך Multi‑LCB מספק הערכה רב‑שפתית מציאותית יותר של יכולות יצירת קוד, ומשמש מדד יציב לפיתוח מודלי קוד שהם באמת language‑agnostic.

<span class="inline-accept">עבודה זו התקבלה ל‑ICLR 2026.<img class="inline-logo" src="./assets/ICLR-logo.svg" alt="ICLR logo" /></span>
מחברים: Maria Ivanova, Pavel Zadorozhny, Rodion Levichev, Ivan Petrov, Pavel Adamenko, Ivan Lopatin, Alexey Kutalev, Dmitrii Babaev