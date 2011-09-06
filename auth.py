from django.conf import settings
from django.contrib.auth.models import User
import urllib2, urllib
from models import AuthToken

class MinecraftBackend:
	supports_object_permissions = False
	supports_anonymous_user = False
	supports_inactive_user = False

	minecraft_version = 99999
	minecraft_login_url = 'https://login.minecraft.net/'
	def authenticate(self, username=None, password=None):
		try:
			f = urllib2.urlopen(self.minecraft_login_url,
				urllib.urlencode([('user',username),('password',password),('version',self.minecraft_version)]))
		except:
			return None
		
		ret = f.readline().strip();
		valid = ret != "Bad login"
		
		if valid:
			items = ret.split(':')
			if ret == "User not premium":
				uname = username
			else:
				uname = items[2]
			
			try:
				user = User.objects.get(username=uname)
				#user.set_password(password)
			except User.DoesNotExist:
				user = User(username=uname,password="a")
				user.save()
				
			if ret != "User not premium":
				try:
					token = user.authtoken
				except AuthToken.DoesNotExist:
					token = AuthToken(user=user)
			
				token.download_ticket = items[1]
				token.session_id = items[3]
				token.latest_version = items[0]			
				token.save()
			
			return user
		return None

	def get_user(self, user_id):
		try:
			return User.objects.get(pk=user_id)
		except User.DoesNotExist:
			return None
