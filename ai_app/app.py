from h2o_wave import Q, app, handle_on, main, on, ui


@app("/")
async def serve(q: Q):
    # First time a browser comes to the app
    if not q.client.initialized:
        await init_app(q)
        q.client.initialized = True

    # Other browser interactions
    await handle_on(q)
    await q.page.save()


async def init_app(q: Q) -> None:
    """Initialize the app for the first page load"""

    # Set default values
    q.client.dark_mode = True

    # Set Title, Theme, and Layout
    q.page["meta"] = ui.meta_card(
        box="",
        title="AI App",
        theme="winter-is-coming" if q.client.dark_mode else "ember",
        layouts=[
            ui.layout(
                breakpoint="xs",
                min_height="100vh",
                max_width="1200px",
                zones=[
                    ui.zone("header"),
                    ui.zone(
                        "content",
                        size="1",
                        zones=[
                            ui.zone("vertical", size="1"),
                        ],
                    ),
                    ui.zone(name="footer"),
                ],
            )
        ],
    )

    # Set Header
    q.page["header"] = ui.header_card(
        box="header",
        title="AI App",
        subtitle="Now running on Heroku",
        image="https://www.h2o.ai/wp-content/themes/h2o2018/templates/dist/images/h2o_logo.svg",
        items=[
            # This button will toggle the dark mode
            ui.mini_button(
                # A handler (an async function with @on() decorator) must be
                # defined to handle the button click event
                name="change_theme",
                icon="ClearNight",
                label="",
            ),
        ],
        color="transparent",
    )

    # Add main content
    q.page["form"] = ui.form_card(
        box="vertical",
        items=[
            ui.text("This is my app!"),
        ],
    )

    # Set Footer
    q.page["footer"] = ui.footer_card(
        box="footer", caption="Made with 💛 using [H2O Wave](https://wave.h2o.ai)."
    )


@on()
async def change_theme(q: Q):
    """Change the app from light to dark mode"""

    # Toggle dark mode
    q.client.dark_mode = not q.client.dark_mode

    # Toggle theme icon
    q.page["header"].items[0].mini_button.icon = (
        "ClearNight" if q.client.dark_mode else "Sunny"
    )

    # Switch theme
    q.page["meta"].theme = "winter-is-coming" if q.client.dark_mode else "ember"
