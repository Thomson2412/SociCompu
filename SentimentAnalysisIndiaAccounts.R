# Set directory
setwd("~/ResMas AI/Social Computing/Project")

# Libraries
library(dplyr)
library(stringr)
library(purrr)
library(sentimentr)
library(ggplot2)
library(tokenizers)
library(stopwords)
library(gridExtra)
library(tm)
library(openxlsx)

# Read in other tweets from 10 India accounts for march to may 2019 and 2020
data1x19 <- read.xlsx("account_2019-03-01_2019-05-31_MongabayIndia.xlsx")
data2x19 <- read.xlsx("account_2019-03-01_2019-05-31_DelhiBreathe.xlsx")
data3x19 <- read.xlsx("account_2019-03-01_2019-05-31_MRTB_India.xlsx")
data4x19 <- read.xlsx("account_2019-03-01_2019-05-31_icareforlungs.xlsx")
data5x19 <- read.xlsx("account_2019-03-01_2019-05-31_ChintanIndia.xlsx")
data6x19 <- read.xlsx("account_2019-03-01_2019-05-31_CSEINDIA.xlsx")
data7x19 <- read.xlsx("account_2019-03-01_2019-05-31_airqualityindia.xlsx")
data8x19 <- read.xlsx("account_2019-03-01_2019-05-31_down2earthindia.xlsx")
data9x19 <- read.xlsx("account_2019-03-01_2019-05-31_Letssavedelhi.xlsx")
data10x19 <- read.xlsx("account_2019-03-01_2019-05-31_moefcc.xlsx")

data1x20 <- read.xlsx("account_2020-03-01_2020-05-31_MongabayIndia.xlsx")
data2x20 <- read.xlsx("account_2020-03-01_2020-05-31_DelhiBreathe.xlsx")
data3x20 <- read.xlsx("account_2020-03-01_2020-05-31_MRTB_India.xlsx")
data4x20 <- read.xlsx("account_2020-03-01_2020-05-31_icareforlungs.xlsx")
data5x20 <- read.xlsx("account_2020-03-01_2020-05-31_ChintanIndia.xlsx")
data6x20 <- read.xlsx("account_2020-03-01_2020-05-31_CSEINDIA.xlsx")
data7x20 <- read.xlsx("account_2020-03-01_2020-05-31_airqualityindia.xlsx")
data8x20 <- read.xlsx("account_2020-03-01_2020-05-31_down2earthindia.xlsx")
data9x20 <- read.xlsx("account_2020-03-01_2020-05-31_Letssavedelhi.xlsx")
data10x20 <- read.xlsx("account_2020-03-01_2020-05-31_moefcc.xlsx")

# Join the data for 2019 and 2020 and select the tweet content column
tweets2019 <- rbind(data1x19, data2x19, data3x19, data4x19, data5x19, data6x19, data7x19, data8x19, data9x19, data10x19)
tweets2020 <- rbind(data1x20, data2x20, data3x20, data4x20, data5x20, data6x20, data7x20, data8x20, data9x20, data10x20)

# Number of tweets for 2019 and 2020
nrow(tweets2019)
nrow(tweets2020)

# Tokenize the tweets for analysis (remove punctuation and numbers, except for # and @)
tokenizeTweets <- function(tweets) {
  for (i in 1:nrow(tweets)) {
    if (length(unlist(strsplit(tweets[i, "tweet"], " "))) == 1) {
      tokenizedTweet <- tokenize_words(tweets[i, "tweet"]) %>% unlist() %>% tolower() %>% removeNumbers()
      tweets[i, "tweet"] <- tokenizedTweet
    } else {
      tokenizedTweet <- tokenize_tweets(tweets[i, "tweet"]) %>% unlist() %>% tolower()  %>% removeNumbers() %>% reduce(paste)
      tweets[i, "tweet"] <- tokenizedTweet
    } 
  }
  return(tweets)
}

tweets2019 <- tokenizeTweets(tweets2019)
tweets2020 <- tokenizeTweets(tweets2020)

# Sentiment analysis (+: positive; -: negative)
sent2019 <- sentiment_by(tweets2019$tweet)
sent2020 <- sentiment_by(tweets2020$tweet)

# Sentiment score metrics
summary(sent2019$ave_sentiment)
summary(sent2020$ave_sentiment)

sentDist2019 <- qplot(sent2019$ave_sentiment, geom = "histogram", binwidth = 0.1, xlab = "", xlim = c(-2, 2))
sentDist2020 <- qplot(sent2020$ave_sentiment, geom = "histogram", binwidth = 0.1, xlab = "", xlim = c(-2, 2))

grid.arrange(arrangeGrob(sentDist2019, top = "2019", bottom = "Sentiment score", left = "Number of tweets"), arrangeGrob(sentDist2020, top = "2020", bottom = "Sentiment score"), nrow = 1, ncol = 2)

# Is there a mean difference in sentiment scores between 2019 and 2020?
t.test(sent2019$ave_sentiment, sent2020$ave_sentiment)

# Look at most frequent words - with stop word removal

## Unigrams
unigramFrequency <- function(tweets) {
  unigrams <- c()
  for (i in 1:nrow(tweets)) {
    unigrams <- c(unigrams, unlist(strsplit(tweets[i, "tweet"], "\\s+")))
  }
  unigrams <- unlist(unigrams)[!(unlist(unigrams) %in% stopwords::stopwords("en"))]
  unigramFreq <- sort(table(unigrams), decreasing = TRUE)
  return(unigramFreq)
}

unigramFreq2019 <- unigramFrequency(tweets2019)
View(unigramFreq2019)
unigramFreq2020 <- unigramFrequency(tweets2020)
View(unigramFreq2020)

##  Bigrams
bigramFrequency <- function(tweets) {
  bigrams <- c()
  for (i in 1:nrow(tweets)) {
    bigrams <- c(bigrams, unlist(tokenize_ngrams(tweets[i, "tweet"], n = 2, n_min = 2,
                                                 stopwords = stopwords::stopwords("en"))))
  }
  bigramFreq <- sort(table(bigrams), decreasing = TRUE)
  return(bigramFreq)
}

bigramFreq2019 <- bigramFrequency(tweets2019)
View(bigramFreq2019)
bigramFreq2020 <- bigramFrequency(tweets2020)
View(bigramFreq2020)