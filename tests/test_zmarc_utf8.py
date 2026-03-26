from PyZ3950 import zmarc


def test_decode_text_round_trips_utf8_transport_octets():
    marc = zmarc.MARC(None, charset="utf-8")

    mojibake = "Â\x88La Divina CommediaÂ\x89"

    assert marc._decode_text(mojibake) == "La Divina Commedia"
