
import streamlit as st
import pandas as pd
import sqlite3
from google import genai
from datetime import date


# Setting up the page
st.set_page_config(
    page_title="Leftover Genius",
    page_icon="🍳",
    layout="wide"
)

DB_FILE = "leftover_genius.db"


# Styling the dashboard
st.markdown("""
<style>
    :root {
        color-scheme: dark;
    }

    [data-testid="stAppViewContainer"],
    [data-testid="stMain"],
    .main {
        background-color: #11131B !important;
        color: #F4F1FA !important;
    }

    [data-testid="stHeader"] {
        background-color: #11131B !important;
    }

    [data-testid="stSidebar"] {
        background-color: #191C28 !important;
    }

    .block-container {
        max-width: 1250px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    h1, h2, h3, h4, h5, h6 {
        color: #F4F1FA !important;
        font-weight: 700 !important;
    }

    p, li, [data-testid="stMarkdownContainer"] {
        color: #D5D2E0 !important;
    }

    [data-testid="stWidgetLabel"] p,
    [data-testid="stWidgetLabel"] label,
    label {
        color: #E9E5F3 !important;
        font-weight: 600 !important;
    }

    [data-testid="stCaptionContainer"] {
        color: #AAA7BA !important;
    }

    [data-testid="stMetric"] {
        background-color: #222635 !important;
        border: 1px solid #393D52 !important;
        padding: 20px !important;
        border-radius: 15px !important;
    }

    [data-testid="stMetricLabel"] {
        color: #C7C2D8 !important;
    }

    [data-testid="stMetricValue"] {
        color: #F4F1FA !important;
    }

    [data-testid="stMetricDelta"] {
        color: #B5A5FF !important;
    }

    input, textarea {
        background-color: #292E3E !important;
        color: #F4F1FA !important;
        border-color: #49445F !important;
    }

    input::placeholder,
    textarea::placeholder {
        color: #AAA7BA !important;
        opacity: 1 !important;
    }

    [data-baseweb="select"] > div {
        background-color: #292E3E !important;
        border-color: #49445F !important;
        color: #F4F1FA !important;
    }

    [data-baseweb="select"] span,
    [data-baseweb="select"] input {
        color: #F4F1FA !important;
    }

    [data-baseweb="popover"],
    [role="listbox"],
    [role="option"] {
        background-color: #222635 !important;
        color: #F4F1FA !important;
    }

    [role="option"]:hover {
        background-color: #39334F !important;
    }

    [data-testid="stDateInput"] input {
        color: #F4F1FA !important;
    }

    [data-testid="stNumberInput"] button {
        background-color: #39334F !important;
        color: #F4F1FA !important;
    }

    [data-testid="stCheckbox"] label,
    [data-testid="stRadio"] label {
        color: #D5D2E0 !important;
    }

    .stButton > button,
    [data-testid="stFormSubmitButton"] button {
        background-color: #B5A5FF !important;
        color: #171322 !important;
        border: 1px solid #B5A5FF !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        min-height: 43px;
        transition: 0.2s ease;
    }

    .stButton > button:hover,
    [data-testid="stFormSubmitButton"] button:hover {
        background-color: #C9BEFF !important;
        border-color: #C9BEFF !important;
    }

    .stButton > button p,
    [data-testid="stFormSubmitButton"] button p {
        color: #171322 !important;
        font-weight: 700 !important;
    }

    [data-testid="stExpander"] {
        background-color: #1B1E2A !important;
        border: 1px solid #393D52 !important;
        border-radius: 12px !important;
    }

    [data-testid="stExpander"] summary,
    [data-testid="stExpander"] summary p {
        color: #F4F1FA !important;
    }

    [data-testid="stDataFrame"] {
        background-color: #1B1E2A !important;
        border: 1px solid #393D52 !important;
        border-radius: 12px !important;
    }

    [data-testid="stAlert"] {
        border-radius: 10px !important;
    }

    [data-testid="stForm"] {
        background-color: #1B1E2A !important;
        border: 1px solid #393D52 !important;
        padding: 20px !important;
        border-radius: 15px !important;
    }

    hr {
        border-color: #393D52 !important;
    }

    .hero {
        background: linear-gradient(120deg, #222635, #302943);
        border: 1px solid #49415F;
        border-radius: 20px;
        padding: 32px;
        margin-bottom: 25px;
    }

    .hero-title {
        color: #F4F1FA !important;
        font-size: 38px;
        font-weight: 800;
        letter-spacing: -1px;
        margin-bottom: 8px;
    }

    .hero-subtitle {
        color: #D5D2E0 !important;
        font-size: 16px;
    }

    .eyebrow {
        color: #B5A5FF !important;
        font-size: 12px;
        font-weight: 800;
        letter-spacing: 2px;
        text-transform: uppercase;
    }

    .section-heading {
        color: #F4F1FA !important;
        font-size: 24px;
        font-weight: 750;
        margin-top: 12px;
        margin-bottom: 5px;
    }

    .section-description {
        color: #AAA7BA !important;
        font-size: 14px;
        margin-bottom: 18px;
    }

    .panel {
        background-color: #1B1E2A;
        border: 1px solid #393D52;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 15px;
    }

    .status-pill {
        display: inline-block;
        background-color: #39304F;
        color: #D5CAFF !important;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 700;
    }

    .footer {
        text-align: center;
        color: #AAA7BA !important;
        font-size: 12px;
        padding-top: 25px;
    }

    .stProgress > div > div > div > div {
        background-color: #B5A5FF !important;
    }

    ::selection {
        background-color: #7864C9;
        color: white;
    }
</style>
""", unsafe_allow_html=True)


# Creating the database and its tables
def initialize_database():
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                quantity REAL NOT NULL,
                unit TEXT NOT NULL,
                expiry TEXT NOT NULL
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                ingredient TEXT NOT NULL,
                quantity REAL NOT NULL,
                unit TEXT NOT NULL
            )
        """)


# Getting the current inventory from the database
def get_inventory():
    with sqlite3.connect(DB_FILE) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT * FROM inventory ORDER BY expiry"
        ).fetchall()

    return [dict(row) for row in rows]


# Saving a new ingredient
def add_ingredient(name, quantity, unit, expiry):
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("""
            INSERT INTO inventory (name, quantity, unit, expiry)
            VALUES (?, ?, ?, ?)
        """, (name, quantity, unit, expiry.isoformat()))


# Removing an ingredient
def remove_ingredient(item_id):
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute(
            "DELETE FROM inventory WHERE id = ?",
            (item_id,)
        )


# Checking how soon an ingredient will expire
def get_expiry_status(expiry):
    expiry_date = date.fromisoformat(expiry)
    days_left = (expiry_date - date.today()).days

    if days_left < 0:
        return "Expired"

    if days_left == 0:
        return "Expires today"

    if days_left <= 3:
        return "Urgent"

    if days_left <= 7:
        return "Use soon"

    return "Fresh"


# Getting the activity history
def get_history():
    with sqlite3.connect(DB_FILE) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT * FROM history ORDER BY id DESC"
        ).fetchall()

    return [dict(row) for row in rows]


# Asking Gemini to suggest ways to use the available ingredients
def generate_recipes(inventory):
    try:
        api_key = st.secrets["GEMINI_API_KEY"]

        client = genai.Client(api_key=api_key)

        inventory_text = ""

        for item in inventory:
            status = get_expiry_status(item["expiry"])

            inventory_text += (
                f"- {item['name']}: {item['quantity']} "
                f"{item['unit']}, expires {item['expiry']}, "
                f"status: {status}\n"
            )

        prompt = f"""
You are Leftover Genius, an AI kitchen inventory and food waste
management assistant for a small restaurant or cafeteria.

Here is the current kitchen inventory:

{inventory_text}

Create exactly 3 practical preparation plans.

For each plan include:
1. Dish or preparation name.
2. Ingredients required.
3. Quantities to use, with units.
4. Estimated servings.
5. Preparation instructions.
6. Which expiring ingredients it helps use.
7. Any ingredients that need to be purchased.

Important rules:
- Prioritize ingredients that are expiring soon.
- Never recommend expired ingredients.
- Do not use more stock than is available.
- Do not assume ingredients exist if they are not listed.
- Keep suggestions practical for a small commercial kitchen.
- Clearly explain if stock is insufficient.
- These are recommendations, not confirmed stock updates.
- A manager must approve a plan before stock changes.

Finish with a short inventory and food-waste summary.

Use clear headings and readable formatting.
"""

        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )

        if not response.text:
            return "Gemini returned an empty response. Please try again."

        return response.text

    except Exception as e:
        return (
            "Gemini could not generate the preparation plans.\n\n"
            f"Error: {str(e)}"
        )


# Updating stock and recording what was used
def update_inventory(usage):
    with sqlite3.connect(DB_FILE) as conn:
        for item_id, used_quantity in usage.items():

            if used_quantity <= 0:
                continue

            item = conn.execute(
                "SELECT * FROM inventory WHERE id = ?",
                (item_id,)
            ).fetchone()

            if item is None:
                continue

            name = item[1]
            available = item[2]
            unit = item[3]

            if used_quantity > available:
                raise ValueError(
                    f"Usage exceeds available stock for {name}."
                )

            remaining = round(available - used_quantity, 3)

            if remaining <= 0:
                conn.execute(
                    "DELETE FROM inventory WHERE id = ?",
                    (item_id,)
                )
            else:
                conn.execute(
                    "UPDATE inventory SET quantity = ? WHERE id = ?",
                    (remaining, item_id)
                )

            conn.execute("""
                INSERT INTO history (date, ingredient, quantity, unit)
                VALUES (?, ?, ?, ?)
            """, (
                date.today().strftime("%d %b %Y"),
                name,
                used_quantity,
                unit
            ))


# Choosing a suitable quantity step
def get_quantity_step(unit):
    if unit in ["pieces", "packets"]:
        return 1.0

    return 0.1


# Starting the database
initialize_database()


# Keeping temporary page information while the app is open
if "recipes" not in st.session_state:
    st.session_state.recipes = ""

if "approved" not in st.session_state:
    st.session_state.approved = False

if "flash_message" not in st.session_state:
    st.session_state.flash_message = ""


# Showing the main heading
st.markdown("""
<div class="hero">
    <div class="eyebrow">AI-powered kitchen management</div>
    <div class="hero-title">🍳 Leftover Genius</div>
    <div class="hero-subtitle">
        Make smarter use of your ingredients.
        Reduce kitchen waste with AI-powered preparation plans.
    </div>
</div>
""", unsafe_allow_html=True)


if st.session_state.flash_message:
    st.success(st.session_state.flash_message)
    st.session_state.flash_message = ""


# Loading the latest inventory
inventory = get_inventory()


# Showing a quick summary of the kitchen stock
total_items = len(inventory)

expiring_items = sum(
    1 for item in inventory
    if 0 <= (
        date.fromisoformat(item["expiry"]) - date.today()
    ).days <= 3
)

expired_items = sum(
    1 for item in inventory
    if (
        date.fromisoformat(item["expiry"]) - date.today()
    ).days < 0
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total ingredients", total_items)

with col2:
    st.metric("Expiring soon", expiring_items)

with col3:
    st.metric("Expired items", expired_items)


st.divider()


# Adding ingredients and showing the current inventory
st.markdown(
    '<div class="section-heading">📦 Kitchen Inventory</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'Add ingredients and keep track of their quantities and expiry dates.'
    '</div>',
    unsafe_allow_html=True
)


with st.form("ingredient_form", clear_on_submit=True):
    st.markdown("#### Add a new ingredient")

    col1, col2 = st.columns(2)

    with col1:
        ingredient_name = st.text_input(
            "Ingredient name",
            placeholder="e.g. Milk, Flour, Eggs"
        )

        ingredient_quantity = st.number_input(
            "Available quantity",
            min_value=0.01,
            value=1.0,
            step=0.5
        )

    with col2:
        ingredient_unit = st.selectbox(
            "Unit",
            ["kg", "grams", "litres", "ml", "pieces", "packets"]
        )

        ingredient_expiry = st.date_input(
            "Expiry date",
            value=date.today()
        )

    add_button = st.form_submit_button(
        "＋ Add to inventory",
        use_container_width=True
    )

    # Saving the ingredient when the form is submitted
    if add_button:
        if ingredient_name.strip():
            add_ingredient(
                ingredient_name.strip(),
                ingredient_quantity,
                ingredient_unit,
                ingredient_expiry
            )

            st.session_state.recipes = ""
            st.session_state.approved = False

            st.session_state.flash_message = (
                f"{ingredient_name.strip()} added to your inventory."
            )

            st.rerun()

        else:
            st.error("Please enter an ingredient name.")


# Loading the inventory again after adding an ingredient
inventory = get_inventory()


# Showing ingredients in order of expiry date
if inventory:
    st.markdown("#### Current stock")

    inventory_data = []

    for item in inventory:
        inventory_data.append({
            "Ingredient": item["name"],
            "Quantity": item["quantity"],
            "Unit": item["unit"],
            "Expiry date": item["expiry"],
            "Status": get_expiry_status(item["expiry"])
        })

    inventory_df = pd.DataFrame(inventory_data)

    st.dataframe(
        inventory_df,
        use_container_width=True,
        hide_index=True
    )

    # Option to remove an ingredient from the list
    with st.expander("Manage inventory"):
        selected_item = st.selectbox(
            "Select an ingredient to remove",
            inventory,
            format_func=lambda item: (
                f"{item['name']} — "
                f"{item['quantity']} {item['unit']}"
            ),
            key="remove_item"
        )

        if st.button("Remove selected ingredient"):
            remove_ingredient(selected_item["id"])

            st.session_state.recipes = ""
            st.session_state.approved = False

            st.session_state.flash_message = (
                f"{selected_item['name']} removed from inventory."
            )

            st.rerun()

else:
    st.info(
        "Your inventory is empty. Add some ingredients to get started."
    )


st.divider()


# Showing the AI preparation planner
st.markdown(
    '<div class="section-heading">✨ AI Preparation Planner</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'Let Gemini analyze your kitchen stock and suggest practical '
    'ways to reduce food waste.'
    '</div>',
    unsafe_allow_html=True
)


if st.button(
    "✨ Generate preparation plans",
    use_container_width=True,
    disabled=len(inventory) == 0
):
    with st.spinner("Gemini is analyzing your kitchen inventory..."):
        st.session_state.recipes = generate_recipes(inventory)
        st.session_state.approved = False


# Showing the suggestions returned by Gemini
if st.session_state.recipes:
    st.markdown("#### Your AI-generated plans")

    st.markdown(
        '<span class="status-pill">GEMINI AI ANALYSIS</span>',
        unsafe_allow_html=True
    )

    st.markdown(st.session_state.recipes)

    st.divider()

    # Manager checks the plan before stock is changed
    st.markdown("#### Manager review")

    st.write(
        "Review the preparation plans above. "
        "Only approve them if they are suitable for your kitchen."
    )

    if not st.session_state.approved:
        if st.button(
            "✓ Approve preparation plan",
            use_container_width=True
        ):
            st.session_state.approved = True
            st.rerun()

    else:
        st.success(
            "Plan approved. You can now record the actual ingredient usage."
        )

        inventory = get_inventory()

        if inventory:
            st.markdown("#### Record actual ingredient usage")

            st.caption(
                "Enter the quantities actually used. "
                "Stock changes only after you confirm."
            )

            with st.form("usage_form"):
                usage = {}

                for item in inventory:
                    step = get_quantity_step(item["unit"])

                    usage[item["id"]] = st.number_input(
                        f"{item['name']} — available: "
                        f"{item['quantity']} {item['unit']}",
                        min_value=0.0,
                        max_value=float(item["quantity"]),
                        value=0.0,
                        step=step,
                        key=f"usage_{item['id']}"
                    )

                confirm_usage = st.form_submit_button(
                    "Confirm usage and update inventory",
                    use_container_width=True
                )

                # Updating stock only when the manager confirms
                if confirm_usage:
                    try:
                        if any(value > 0 for value in usage.values()):
                            update_inventory(usage)

                            st.session_state.recipes = ""
                            st.session_state.approved = False

                            st.session_state.flash_message = (
                                "Inventory and activity history updated!"
                            )

                            st.rerun()

                        else:
                            st.warning(
                                "Enter at least one quantity before confirming."
                            )

                    except Exception as e:
                        st.error(f"Could not update inventory: {str(e)}")


st.divider()


# Showing previous stock updates
st.markdown(
    '<div class="section-heading">📋 Activity History</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'A record of ingredient quantities confirmed as used.'
    '</div>',
    unsafe_allow_html=True
)

history = get_history()

if history:
    history_df = pd.DataFrame(history)

    history_df = history_df.rename(columns={
        "date": "Date",
        "ingredient": "Ingredient",
        "quantity": "Quantity used",
        "unit": "Unit"
    })

    st.dataframe(
        history_df[[
            "Date",
            "Ingredient",
            "Quantity used",
            "Unit"
        ]],
        use_container_width=True,
        hide_index=True
    )

else:
    st.caption("No inventory updates have been recorded yet.")


# Small footer at the bottom of the page
st.markdown("""
<div class="footer">
    LEFTOVER GENIUS · SMARTER KITCHENS · LESS FOOD WASTE
    <br>
    Powered by Streamlit, SQLite and Google Gemini
</div>
""", unsafe_allow_html=True)
