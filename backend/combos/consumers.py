# chat/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.serializers import serialize

import json
#===========================
from delve import models
import pandas as pd
import numpy as np
from helper import plot, tox_plot
import ast

from ada.forms import Upload_Form
#===========================
# from channels.consumer import AsyncConsumer
# load and evaluate a saved model


class ComboConsumer(AsyncWebsocketConsumer):
	
	async def connect(self):
		# res = models.Combo.objects.latest('id')
		# df = res.get_df()
		# arr = np.array(df.apply(pd.to_numeric).values.tolist())
		# fig = plot.ic50_graph(res.get_df(), 0)

		# load model

		# drugs = ["Paclitaxel", "Etoposide"]
		# target = []
		# NN_model.evaluate(drugs, target, steps=None)
		await self.accept()


	async def receive(self, text_data):
		print('================================')
		print(text_data)	
		if 'panel-submit' in text_data:
		
			res = models.Combo.objects.latest('id')
			df = res.get_df()		
			fig = plot.get_combo(df)	
				
			if "Indications" in text_data:
				fig = plot.ic50_graph(df)
			elif "Neural Net. Model" in text_data:
				fig = plot.get_combo(df)
			elif "IC50":
				fig = plot.ic50_graph(df)
			else:
				fig = None
			await self.send(text_data=json.dumps({
			'figure': fig
			}))

		# failing to send models objects over websocket
		elif 'selecting-visual' in text_data:
			if "Indications" in text_data:
				head = "Indications"
				# obj = models.Combos.objects.get(pk=1)
			elif "Neural Net. Model" in text_data:
				head = "NN Model"
				# obj = models.Combos.objects.get(pk=1)
			else: # IC50
				head = "IC50"
				# obj = models.Drug.objects.all		
			# print('sending obj:', msg) 
			obj = "hi"
			# await self.send(text_data=json.dumps({
			# 	head: serialize('json', obj)
			# }))
			# serialize('json', SomeModel.objects.all(), cls=LazyEncoder)

		
	async def disconnect(self, close_code):
		print("disconneted, retrying")
		self.connect()

	
	