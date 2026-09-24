from flask import Flask, render_template, request, session, jsonify
from datetime import datetime
import itertools

app = Flask(__name__)
app.secret_key = "baifern-cafe-dev-secret"  # เปลี่ยนเป็นค่าอื่นก่อนใช้งานจริง

# ---------------- เมนูและตัวเลือกเสริม ----------------
SUGAR_OPTS = ["หวานปกติ", "หวานน้อย 50%", "หวานน้อย 25%", "ไม่หวาน"]
ICE_OPTS = ["น้ำแข็งปกติ", "น้ำแข็งน้อย", "ไม่ใส่น้ำแข็ง"]

DRINK_TOPPINGS = [
    {"name": "ไข่มุก", "price": 10},
    {"name": "วิปครีมสด", "price": 15},
    {"name": "เยลลี่ลิ้นจี่", "price": 10},
    {"name": "ชอตกาแฟเพิ่ม", "price": 20},
]
BAKERY_TOPPINGS = [
    {"name": "ไอศกรีมสกู๊ป", "price": 25},
    {"name": "ซอสช็อกโกแลต", "price": 10},
    {"name": "วิปครีมสด", "price": 15},
]

MENU = [
    {"id": 1, "cat": "กาแฟร้อน", "name": "เอสเปรสโซ", "desc": "เข้มข้น หอมกลิ่นคั่วเข้ม", "price": 55, "emoji": "☕", "bg": "#EFE3CC", "sugar": True, "ice": False, "toppings": DRINK_TOPPINGS},
    {"id": 2, "cat": "กาแฟร้อน", "name": "ลาเต้ร้อน", "desc": "นมสตีมเนียนนุ่ม", "price": 65, "emoji": "☕", "bg": "#EFE3CC", "sugar": True, "ice": False, "toppings": DRINK_TOPPINGS},
    {"id": 3, "cat": "กาแฟร้อน", "name": "อเมริกาโน่ร้อน", "desc": "บางเบา ดื่มง่าย", "price": 55, "emoji": "☕", "bg": "#EFE3CC", "sugar": True, "ice": False, "toppings": DRINK_TOPPINGS},
    {"id": 4, "cat": "กาแฟเย็น", "name": "ลาเต้เย็น", "desc": "หวานมันกำลังดี เสิร์ฟเย็นฉ่ำ", "price": 70, "emoji": "🧊", "bg": "#DCEAE2", "sugar": True, "ice": True, "toppings": DRINK_TOPPINGS},
    {"id": 5, "cat": "กาแฟเย็น", "name": "อเมริกาโน่เย็น", "desc": "เข้ม สดชื่น", "price": 60, "emoji": "🧊", "bg": "#DCEAE2", "sugar": True, "ice": True, "toppings": DRINK_TOPPINGS},
    {"id": 6, "cat": "กาแฟเย็น", "name": "ดัลโกน่าเย็น", "desc": "ตีฟองนมหนานุ่ม", "price": 75, "emoji": "🧊", "bg": "#DCEAE2", "sugar": True, "ice": True, "toppings": DRINK_TOPPINGS},
    {"id": 7, "cat": "ชา", "name": "ชาไทยเย็น", "desc": "หอมกลิ่นใบชา หวานมัน", "price": 60, "emoji": "🍵", "bg": "#F3D9B8", "sugar": True, "ice": True, "toppings": DRINK_TOPPINGS},
    {"id": 8, "cat": "ชา", "name": "ชามะนาว", "desc": "เปรี้ยวสดชื่น", "price": 55, "emoji": "🍵", "bg": "#F3D9B8", "sugar": True, "ice": True, "toppings": DRINK_TOPPINGS},
    {"id": 9, "cat": "ชา", "name": "มัทฉะลาเต้", "desc": "ชาเขียวญี่ปุ่นแท้", "price": 75, "emoji": "🍵", "bg": "#DCE7C8", "sugar": True, "ice": True, "toppings": DRINK_TOPPINGS},
    {"id": 10, "cat": "เบเกอรี่", "name": "ครัวซองต์เนย", "desc": "อบใหม่ทุกเช้า กรอบนอกนุ่มใน", "price": 55, "emoji": "🥐", "bg": "#F1DCB8", "sugar": False, "ice": False, "toppings": BAKERY_TOPPINGS},
    {"id": 11, "cat": "เบเกอรี่", "name": "บานอฟฟี่พาย", "desc": "กล้วย คาราเมล ครีมสด", "price": 85, "emoji": "🥧", "bg": "#F1DCB8", "sugar": False, "ice": False, "toppings": BAKERY_TOPPINGS},
    {"id": 12, "cat": "เบเกอรี่", "name": "บราวนี่ช็อกโกแลต", "desc": "เข้มข้น หนึบหนับ", "price": 65, "emoji": "🍫", "bg": "#E4CBB4", "sugar": False, "ice": False, "toppings": BAKERY_TOPPINGS},
]
CATEGORIES = ["ทั้งหมด"] + list(dict.fromkeys(m["cat"] for m in MENU))
MENU_BY_ID = {m["id"]: m for m in MENU}

# ---------------- ที่เก็บข้อมูล (in-memory เดโมเท่านั้น — รีสตาร์ตแอปแล้วข้อมูลหาย) ----------------
orders = []
order_seq = itertools.count(1001)

STATUSES = ["รอดำเนินการ", "กำลังทำ", "เสร็จแล้ว"]
NEXT_STATUS = {"รอดำเนินการ": "กำลังทำ", "กำลังทำ": "เสร็จแล้ว"}


def get_cart():
    return session.setdefault("cart", [])


def cart_total(cart):
    return sum(line["line_total"] for line in cart)


def line_opts_text(line):
    parts = []
    if line.get("sugar"):
        parts.append(line["sugar"])
    if line.get("ice"):
        parts.append(line["ice"])
    if line.get("toppings"):
        parts.append("เพิ่ม: " + ", ".join(line["toppings"]))
    return " · ".join(parts)


# ---------------- หน้าเว็บ ----------------
@app.route("/")
def index():
    active_cat = request.args.get("cat", "ทั้งหมด")
    items = MENU if active_cat == "ทั้งหมด" else [m for m in MENU if m["cat"] == active_cat]
    cart = get_cart()
    in_cart_counts = {}
    for line in cart:
        in_cart_counts[line["item_id"]] = in_cart_counts.get(line["item_id"], 0) + line["qty"]
    return render_template(
        "index.html",
        categories=CATEGORIES,
        active_cat=active_cat,
        items=items,
        in_cart_counts=in_cart_counts,
        cart_count=sum(l["qty"] for l in cart),
        menu_json=MENU,
        sugar_opts=SUGAR_OPTS,
        ice_opts=ICE_OPTS,
    )


@app.route("/owner")
def owner():
    return render_template("owner.html", statuses=STATUSES)


# ---------------- API: ตะกร้า ----------------
@app.route("/api/cart", methods=["GET"])
def api_get_cart():
    cart = get_cart()
    return jsonify(cart=cart, total=cart_total(cart), count=sum(l["qty"] for l in cart))


@app.route("/api/cart/add", methods=["POST"])
def api_add_to_cart():
    data = request.get_json(force=True)
    item = MENU_BY_ID.get(int(data.get("item_id", 0)))
    if not item:
        return jsonify(error="ไม่พบเมนูนี้"), 404

    qty = max(1, int(data.get("qty", 1)))
    sugar = data.get("sugar") if item["sugar"] else None
    ice = data.get("ice") if item["ice"] else None
    valid_topping_names = {t["name"] for t in item["toppings"]}
    toppings = [t for t in data.get("toppings", []) if t in valid_topping_names]

    extra = sum(t["price"] for t in item["toppings"] if t["name"] in toppings)
    unit_price = item["price"] + extra

    cart = get_cart()
    next_uid = (max((l["uid"] for l in cart), default=0)) + 1
    cart.append({
        "uid": next_uid,
        "item_id": item["id"],
        "name": item["name"],
        "emoji": item["emoji"],
        "bg": item["bg"],
        "qty": qty,
        "sugar": sugar,
        "ice": ice,
        "toppings": toppings,
        "unit_price": unit_price,
        "line_total": unit_price * qty,
    })
    session["cart"] = cart
    session.modified = True
    return jsonify(cart=cart, total=cart_total(cart), count=sum(l["qty"] for l in cart))


@app.route("/api/cart/remove/<int:uid>", methods=["POST"])
def api_remove_from_cart(uid):
    cart = [l for l in get_cart() if l["uid"] != uid]
    session["cart"] = cart
    session.modified = True
    return jsonify(cart=cart, total=cart_total(cart), count=sum(l["qty"] for l in cart))


@app.route("/api/checkout", methods=["POST"])
def api_checkout():
    cart = get_cart()
    if not cart:
        return jsonify(error="ตะกร้าว่าง"), 400

    data = request.get_json(force=True)
    order = {
        "id": next(order_seq),
        "name": (data.get("name") or "").strip() or "ลูกค้าไม่ระบุชื่อ",
        "phone": (data.get("phone") or "").strip(),
        "fulfil": data.get("fulfil") or "รับที่ร้าน",
        "pay": data.get("pay") or "เงินสดหน้าร้าน",
        "note": (data.get("note") or "").strip(),
        "items": [
            {
                "name": l["name"],
                "qty": l["qty"],
                "unit_price": l["unit_price"],
                "line_total": l["line_total"],
                "opts": line_opts_text(l),
            }
            for l in cart
        ],
        "total": cart_total(cart),
        "status": STATUSES[0],
        "time": datetime.now().strftime("%H:%M"),
    }
    orders.insert(0, order)
    session["cart"] = []
    session.modified = True
    return jsonify(order=order)


# ---------------- API: เจ้าของร้าน ----------------
@app.route("/api/orders", methods=["GET"])
def api_orders():
    sales = sum(o["total"] for o in orders)
    pending = sum(1 for o in orders if o["status"] != STATUSES[-1])
    return jsonify(orders=orders, sales=sales, order_count=len(orders), pending=pending)


@app.route("/api/orders/<int:order_id>/advance", methods=["POST"])
def api_advance_order(order_id):
    for o in orders:
        if o["id"] == order_id:
            o["status"] = NEXT_STATUS.get(o["status"], "กำลังทำ")
            break
    return jsonify(orders=orders)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
