def increment_helpdesk_number():
    last_helpdesk = helpdesk.objects.all().order_by('id').last()

    if not last_helpdesk:
        return 'HEL-' + str(datetime.now().strftime('%Y%m%d-')) + '0000'

    help_id = last_helpdesk.help_num
    help_int = help_id[13:17]
    new_help_int = int(help_int) + 1
    new_help_id = 'HEL-' + str(datetime.now().strftime('%Y%m%d-')) + str(new_help_int).zfill(4)

    return new_help_id