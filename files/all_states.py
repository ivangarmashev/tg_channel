from files.bot_states import States

all_state = (States.menu, States.select_in_schedule, States.sent,
             States.sent, States.add_photo, States.add_text,
             States.add_photo, States.add_name, States.add_hyperlinks,
             States.add_link, States.add_schedule, States.edit_time, States.show)

without_name = (States.menu, States.select_in_schedule, States.sent,
                States.sent, States.add_photo, States.add_text,
                States.add_photo, States.add_hyperlinks, States.add_link,
                States.add_schedule, States.edit_time, States.show)

without_text = (States.menu, States.select_in_schedule, States.sent,
                States.sent, States.add_photo, States.add_name,
                States.add_photo, States.add_hyperlinks, States.add_link,
                States.add_schedule, States.edit_time, States.show)

without_hyperlinks = (States.menu, States.select_in_schedule, States.sent,
                      States.sent, States.add_photo, States.add_name,
                      States.add_photo, States.add_text, States.add_link,
                      States.add_schedule, States.edit_time, States.show)
