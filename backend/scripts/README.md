# Backend Scripts

سكربتات تشغيلية للـ backend (تهيئة البيانات، إعادة تعيين كلمة المرور، إلخ).

## التشغيل

يجب تشغيل السكربتات من مجلد `backend` حتى يتم حل استيراد `app` بشكل صحيح:

```bash
cd backend
source venv/bin/activate   # أو تفعيل البيئة الافتراضية
```

---

## Seed (تهيئة البيانات)

لتهيئة قاعدة البيانات بغرف ومنتجات ومراجعات تجريبية:

```bash
python -m app.core.seed_data
```

أو:

```bash
python -c "import asyncio; from app.core.seed_data import seed_all; asyncio.run(seed_all())"
```

---

## Reset Admin Password

إعادة تعيين كلمة مرور حساب المدير (admin@alkhayma.com):

```bash
python scripts/reset_admin.py
```

يُفضّل تعيين كلمة المرور الجديدة عبر متغير البيئة:
`ADMIN_NEW_PASSWORD=your_new_password python scripts/reset_admin.py`

---

## سكربتات أرشفة

السكربتات القديمة أو المؤقتة (مثل seed_database.py، validate_*.py) موجودة في `scripts/archive/` للرجوع إليها فقط ولا يُنصح باستخدامها في التطوير الجديد.
