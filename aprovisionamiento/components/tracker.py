from typing import List, Literal, TypedDict


class TrackerStep(TypedDict):
    label: str
    date: str
    state: Literal["done", "active", ""]


def tracker(steps: List[TrackerStep]) -> str:
    items = ""
    for s in steps:
        knob = ""
        if s["state"] == "done":
            knob = '<svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><path d="m20 6-11 11-5-5"/></svg>'
        elif s["state"] == "active":
            knob = '<span style="width:8px;height:8px;border-radius:50%;background:currentColor;display:block;"></span>'
        items += f"""
        <div class="al-trk {s['state']}">
          <div class="knob">{knob}</div>
          <div class="lbl">{s['label']}</div>
          <div class="date">{s['date']}</div>
        </div>
        """
    return f'<div class="al-tracker">{items}</div>'
