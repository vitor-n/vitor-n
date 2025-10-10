import yaml
from datetime import datetime
import os
import drawsvg as svg

from src.utils import *
from src.github_stats import *

WIDTH, HEIGHT = 985, 570
MY_BIRTHDAY = datetime(2004, 8, 14)
USER = "vitor"  
HOST = "nascimento"

n_repos = get_user_profile(USER_NAME)["public_repos"]
n_commits = get_commit_count(USER_NAME)

repos = get_all_repos(USER_NAME)
source_repos = [repo for repo in repos if not repo['fork']]

style_block = \
    """
    <style>
        @font-face {
            src: local("Consolas"), local("Consolas Bold");
            font-family: "ConsolasFallback";
            font-display: swap;
            -webkit-size-adjust: 109%;
            size-adjust: 109%;
        }
        .key { fill: #70c0b1; font-weight: bold; }
        .value { fill: #a1a1a1; }
        .title { fill: #fe8019; font-weight: bold; }
        .prompt-user { fill: #b8bb26; }
        .dots { fill: #928374 }
        .ascii { fill: #928374 }
        .green { fill: #b8bb26 }
        text, tspan { white-space: pre; fill: #c9d1d9; font-size: 16 }
        @keyframes blink {
            50% { opacity: 0; }
            100% { opacity: 1; }
        }
        #cursor {
            animation: blink 1s step-end infinite;
        }
    </style>
    """

def text(text, x, y, font_size=16, **kwargs):
    return svg.Text(text, font_size, x=x, y=y, **kwargs)

if __name__ == "__main__":
    stream = open("info.yaml", "r")
    parsed_data = yaml.safe_load_all(stream)

    d = svg.Drawing(WIDTH, HEIGHT, font_family="ConsolasFallback, Consolas, monospace", font_size="16px")
    d.append(svg.Raw(style_block))
    d.append(svg.Rectangle(0, 0, "100%", "100%", rx=25, fill="#1c1c1c"))

    cursor = Cursor((25, 70))
    icon = next(parsed_data)["icon"]
    for line in icon.split("\n"):
        d.append(text(line[1:-1], x=cursor.get_x(), y=cursor.jump_line(), class_="ascii"))

    cursor.set_pos((405, 30))
    parsed_data = next(parsed_data)

    header = text("", x=405, y=cursor.jump_line())
    header.append(svg.TSpan(f"{USER}", class_="key"))
    header.append(svg.TSpan("@"))
    header.append(svg.TSpan(f"{HOST}", class_="key"))

    d.append(header)
    d.append(text("-"*(len(USER)+len(HOST)+1), x=405, y=cursor.jump_line()))
    cursor.jump_line()

    for title, content in parsed_data.items():
        title_line = text("", x=cursor.get_x(), y=cursor.jump_line())
        title_line.append(svg.TSpan(title, class_="title"))

        d.append(title_line)

        for item in content:
            for key, value in item.items():
                if key == "Uptime":
                    value = get_time_since(MY_BIRTHDAY)
                elif isinstance(value, list):
                    value = ", ".join(map(str, value))
                else:
                    value = str(value)

                line = format_line(cursor, key, value)
                d.append(line)

        cursor.jump_line()

    title_line = text("", x=cursor.get_x(), y=cursor.jump_line())
    title_line.append(svg.TSpan("Github Statistics", class_="title"))
    d.append(title_line)

    line = format_line(cursor, "Repos", n_repos)
    d.append(line)

    line = format_line(cursor, "Commits", n_commits)
    d.append(line)

    cursor.set_pos((15, 550))

    line = text("", x=cursor.get_x(), y=cursor.jump_line())
    line.append(svg.TSpan(f"{USER}", class_="green"))
    line.append(svg.TSpan(f"@"))
    line.append(svg.TSpan(f"{HOST}"))
    line.append(svg.TSpan(f" ~", class_="green"))
    line.append(svg.TSpan(f">"))
    line.append(svg.TSpan(f" █", id_="cursor"))
    d.append(line)

    d.save_svg("info.svg")
    cursor.reset()