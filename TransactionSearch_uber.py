#!/usr/bin/env python

# Uber test account API credentials
# USER:		paypal-apiactor_api1.uber.com
# PWD:  	EJ3XQ4FJW4TE55KK
# SIGNATURE: 	AFcWxV21C7fd0v3bYYYRCpSSRl31AZyxX9dm9rylg.u9qWPJX5ow0nIq

# Uber test accounts
# US:	paypal-us@uber.com
# DE: 	paypal-de@uber.com
# NL:	paypal-nl@uber.com
# FR: 	paypal-fr@uber.com
# IT:	paypal-it@uber.com

# some source code borrowed from http://pastebin.com/f782d48d9 and modified


import urllib, md5, datetime, pprint

class PayPal:
  """ #PayPal utility class"""
  signature_values = {}
  API_ENDPOINT = ""
 
  def __init__(self):
      # API credentials and API version
      self.signature_values = {
      'USER' : 'paypal-apiactor_api1.uber.com', 
      'PWD' : 'EJ3XQ4FJW4TE55KK', 
      'SIGNATURE' : 'AFcWxV21C7fd0v3bYYYRCpSSRl31AZyxX9dm9rylg.u9qWPJX5ow0nIq', 
      'VERSION' : '106.0',
      }
      self.API_ENDPOINT = 'https://api.stage2ms059.stage.paypal.com/nvp' # test environment URL, not production
      self.signature = urllib.urlencode(self.signature_values) + "&"
  
  def InvokeAPI(self, params):
      request = self.signature + urllib.urlencode(params)
      response = urllib.urlopen(self.API_ENDPOINT, request).read()
      response_tokens = {}
      for token in response.split('&'):
              response_tokens[token.split("=")[0]] = token.split("=")[1]
      for key in response_tokens.keys():
                      response_tokens[key] = urllib.unquote(response_tokens[key])
      # Need to include error handling if API returns Ack=Failure
      return response_tokens

  # uber_account_email - email associated with the PayPal account for a specific country (e.g. paypal-us@uber.com)
  def TransactionSearch (self, uber_account_email, customer_email, start_date='2013-10-15T00:00:00Z', end_date='2013-10-16T00:00:00Z'):
      params = {
              'METHOD' : "TransactionSearch",
              'SUBJECT' : uber_account_email,
              'STARTDATE' : start_date,
              'ENDDATE' : end_date,
              'EMAIL' : customer_email,
      } 
      return self.InvokeAPI(params)

  def GetTransactionDetails(self, uber_account_email, txn_id):
      params = {
              'METHOD' : "GetTransactionDetails",
              'SUBJECT' : uber_account_email,
              'TRANSACTIONID' : txn_id,
      }
      return self.InvokeAPI(params)

                     
paypal=PayPal()

# Search transactions by customer email in the Dutch account
transactions=paypal.TransactionSearch('paypal-nl@uber.com','tnm10@paypal.com')
# Some logic is needed to handle transactions['Ack']=='Failure' scenario (which means API call failed)
# Some logic is needed to handle transactions['SuccessWithWarning'] scenario which means the result set was truncated to first 100 transactions. This means the timeframe for TransactionSearch request needs to be shortened


# this will return no results because the accounts don't have transactions from 2012
# transactions=paypal.TransactionSearch('paypal-nl@uber.com','tnm10@paypal.com','2012-10-01T00:00:00Z','2012-10-14T00:00:00Z')

col_size=25
print 'TIME'.ljust(col_size) + 'TRANSACTIONID'.ljust(col_size) + 'STATUS'.ljust(col_size) + 'TRANSACTIONTYPE'.ljust(col_size) + 'AMOUNT'.ljust(col_size) + 'CURRENCY'.ljust(col_size)
i=0
while True :
  if "L_TIMESTAMP"+str(i) in transactions :
     print transactions['L_TIMESTAMP'+str(i)].ljust(col_size) + transactions['L_TRANSACTIONID'+str(i)].ljust(col_size) + transactions['L_STATUS'+str(i)].ljust(col_size) + transactions['L_TYPE'+str(i)].ljust(col_size) + transactions['L_AMT'+str(i)] .ljust(col_size) + transactions['L_CURRENCYCODE'+str(i)].ljust(col_size)
     i += 1
  else :
     break

# get details of a specific transaction id
txn_details=paypal.GetTransactionDetails('paypal-nl@uber.com','00H68298G7968670S')
pp=pprint.PrettyPrinter(indent=4)
pp.pprint(txn_details)
