from GEC_python import predict

text = "I wonder if I should take a risk"
out = predict(text)
out2 = str(out)
print("output is: ", out)
print("output without brackets is: ", out2[2:-8])
