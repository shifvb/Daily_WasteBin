import os
import sys
sys.path.append(os.path.abspath("."))
from _server_side import SignalMessageReceiver, ReceiveFileParser


def main():
    smr = SignalMessageReceiver(debug=True)
    smr.listen(parsers=[ReceiveFileParser])


if __name__ == '__main__':
    main()
