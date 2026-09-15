from gigachat import GigaChat

GIGACHAT_TOKEN = "MDE5ZmQ4OGItYzdjOC03N2JiLWFlZmEtZDA1NDU4NzBmZTg3OmFmYjE4MzY1LTBmMWYtNGJmOC1iNTJhLThlMTE2NjQyMDUxMQ=="

giga = GigaChat(credentials=GIGACHAT_TOKEN, verify_ssl_certs=False)

models = giga.get_models()
for model in models.data:
    print(model.id_)