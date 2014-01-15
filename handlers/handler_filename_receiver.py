import os
from kivy import Logger
from twisted.internet import reactor
from twisted.internet.protocol import ClientCreator
from twisted.protocols.basic import NetstringReceiver
import json
from handlers.handler_tcp_message_sender import TCPSender, sendMessage, printError

class FilenameReceiverServer(NetstringReceiver):

	MAX_LENGTH = 99999999 # set to something insanely high, change from default of 99999
	# a raw 1080p screenshot is like 11mb (damn!) ~ 11059227 numbers or more

	def stringReceived(self, string):
		phone_data = json.loads(string)

		user      = phone_data["user"]
		directory = phone_data["directory"]
		filename  = phone_data["filename"]
		raw_data  = phone_data["raw_data"]
		has_raw_data = phone_data["has_raw_data"]

		Logger.debug("FilenameReceiver Server: received: {0}, {1}, {2}, {3}".format(user, directory, filename, has_raw_data))

		# Save the file to disk (if we have the file data)
		if has_raw_data == "1":
			image_data = raw_data.decode('base64')
			folder_path = os.getcwd() + os.sep + "received_files" + os.sep + directory
			if not os.path.exists(folder_path):
				os.makedirs(folder_path)

			f = open(folder_path+os.sep+filename, 'wb')
			f.write(image_data)
			f.close()
			Logger.debug("FilenameReceiver Server: wrote image file to, received_files/{0}/{1}".format(directory, filename))

		# Do something here, in terms of logic (assuming received the file).
		result = self.app_root.root.process_image_from_phone(int(user), folder_path+os.sep+filename, filename)
		if result is True:
			# Send an ack back to the computer (or phone), with the filename
			source = self.transport.getPeer() # retrieve the ip of the computer that sent us the payload

			output = {"filename": filename}
			line = json.dumps(output)
			ClientCreator(reactor, TCPSender).connectTCP(source.host, 7895).addCallback(sendMessage, "{0}".format(line)).addErrback(printError)

