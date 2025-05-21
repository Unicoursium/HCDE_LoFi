from gpiozero import LED
from time import sleep

# ³õʼ»¯ GPIO26 ΪÊä³ö£¬¿ØÖÆһ¸ö LED »òÆäËû¸ºÔØ
led = LED(26)

# ´ò¿ª GPIO26£¨Êä³ö¸ߵçƽ£©
led.on()
print("GPIO26 opened")

# ±£³Ö5Ãë
sleep(5)

# ¹رÕ GPIO26£¨Êä³öµ͵çƽ£©
led.off()
print("GPIO26 closed")

