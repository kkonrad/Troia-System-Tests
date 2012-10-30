

def get_troia_client(url="http://localhost:8080/GetAnotherLabel/rest"):
    from troia_client import TroiaClient
    return TroiaClient(url, None)


def prepare_troia_client(jid, correct, costs):
    tc = get_troia_client()
    tc.reset(jid)
    tc.load_categories(costs, jid)
    tc.load_gold_labels(correct, jid)
    return tc
