def hero_card(code: str, title: str, meta_items: list, amount: dict) -> str:
    meta_html = "".join(
        f'<span>{lbl} <b>{val}</b></span>' for lbl, val in meta_items
    )
    return f"""
    <div class="al-hero">
      <div>
        <div class="al-hero-code">{code}</div>
        <div class="al-hero-title">{title}</div>
        <div class="al-hero-meta">{meta_html}</div>
      </div>
      <div class="al-hero-amount">
        <div class="l">{amount['label']}</div>
        <div class="v">{amount['value']}</div>
        <div class="s">{amount.get('sub', '')}</div>
      </div>
    </div>
    """
