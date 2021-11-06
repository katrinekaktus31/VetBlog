from django.core.mail import send_mail


def send_to_vet_member(client_email, text_email, client_name):
    """ send mail to veb portal email with required inf about client"""
    send_mail(
        f"Онлайн консультація репродукції тварин НУБіП для  {client_name}. Email: {client_email}",
        text_email,
        'vetReproductionNUBip@gmail.com',
        ['vetReproductionNUBip@gmail.com'],

    )


def send_to_user(client_email, ):
    """ send successes email to client"""
    send_mail(
        "Онлайн консультації репродукції тварин НУБіП",
        "Ви успішно залишили заявку на онлайн консультацію з нашем ветеринарним лікарем-акушером. Ми зв'яжемося з "
        "Вами найближчим "
        "часом! ",
        'vetReproductionNUBip@gmail.com',
        [client_email],
        fail_silently=True,
    )
