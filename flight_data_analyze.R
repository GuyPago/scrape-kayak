library(dplyr)
library(readr)
library(tidyverse)
library(xtable)
library(stargazer)
df <- read_csv('Data/FlightData_08.06.21_TLV-HNL.csv')

df <- df %>%
  mutate(Hours = Time_min / 60) %>%
  rename(airline = Airline)

df %>%
  filter(Stops == 'n') %>%
  ggplot(mapping = aes(x=Hours, y=Price_ILS)) +
  geom_point() +
  geom_smooth(method = 'lm', se = FALSE, color='blue', size=0.1)


df_non_stop <- df %>%
  filter(Stops == 'n') %>%
  mutate(Weekday = factor(Weekday)) %>%
  filter(!str_detect(airline, ','))


model_1_AllAirports_and_weekday <- lm(Price_ILS ~ Hours , df_non_stop)
summary(model_1_AllAirports_and_weekday)

df_test <- df_non_stop %>%
  filter(!airline %in% c('Air Malta','airBaltic', 'Virgin Atlantic','British Airways',
                         'Brussels airlines','Bulgaria Air','Corendon','Cyprus Airways',
                         'Czech airlines','Etihad Airways','Finnair','FLYONE ',
                         'KLM','LOT','Nordwind airlines','Norwegian','SkyUp','Smartwings',
                         'Transavia France','TAROM','United airlines','Alitalia','FLYONE'
                         ,'Air Canada','Air Europa','Air Moldova','Air France'))

model_2_drop_two_airports <- lm(Price_ILS ~ Hours + airline, df_test)
summary(model_2_drop_two_airports)
  
# We show that the variance is very high between different airlines.
df_test %>%
  ggplot(mapping=aes(x=Hours, y=Price_ILS, colour=airline)) +
  geom_point() +
  theme(legend.key.size = unit(0.05, 'cm'),
        legend.position = 'bottom',
        legend.text = element_text(size = 6.5))

  #geom_smooth(method = 'lm', se = FALSE)

df_Israel_airlines <- df_non_stop %>%
  filter(airline %in% c('EL AL', 'Arkia', 'ISRAIR'), Price_ILS < 2650) 

model_3_Israel_airlines_All_Weekdays <- lm(Price_ILS ~ Hours + airline + Weekday, df_Israel_airlines)
summary(model_3_Israel_airlines_All_Weekdays)

# Average price per weekday
tst <- df_Israel_airlines %>%
  group_by(Weekday) %>%
  summarize(avg_price = mean(Price_ILS))

df_Israel_airlines <- df_Israel_airlines %>%
  mutate(is_WD_4 = as.numeric(Weekday == 4),
         is_WD_6 = as.numeric(Weekday == 6))

model_4_Israel_airlines_Weekday_4_6 <- lm(Price_ILS ~ Hours + airline  + is_WD_4 + is_WD_6, df_Israel_airlines)
summary(model_4_Israel_airlines_Weekday_4_6)

model_5_Israel_Weekday_4_6 <- lm(Price_ILS ~ Hours + weekday_4 + weekday_6, df_Israel_airlines)
summary(model_5_Israel_Weekday_4_6)


df_non_stop %>%
  group_by(airline) %>%
  mutate(price_per_hour = Price_ILS / Hours) %>%
  summarize(avg_price_per_hour = mean(price_per_hour)) %>%
  arrange(avg_price_per_hour) %>%
  summarize(avg = mean(avg_price_per_hour), med = median(avg_price_per_hour), std = sd(avg_price_per_hour))

df_Median_airlines <- df_non_stop %>%
  group_by(airline) %>%
  mutate(price_per_hour = Price_ILS / Hours) %>%
  mutate(avg_price_per_hour = mean(price_per_hour)) %>%
  filter(avg_price_per_hour > 103, avg_price_per_hour <216, Price_ILS < 3000) %>%
  mutate(is_WD_4 = as.numeric(Weekday == 4),
         is_WD_6 = as.numeric(Weekday == 6))

df_Median_airlines %>%
  ggplot(mapping = aes(x=Hours, y=Price_ILS)) +
  geom_point() +
  geom_smooth(method = 'lm', se = FALSE)

df_Median_airlines %>%
  group_by(Weekday) %>%
  summarize(mean(Price_ILS))
  
# Best model yet
model_6_Median_airlines <- lm(Price_ILS ~ Hours + is_WD_4 + is_WD_6, df_Median_airlines)
summary(model_6_Median_airlines)

model_7_Median_airlines_Weekdays <- lm(Price_ILS ~ Hours + is_WD_4 + is_WD_6 + airline, df_Median_airlines)
summary(model_7_Median_airlines_Weekdays)  

df_filter_airlines <- df_Median_airlines %>%
  filter(!airline %in% c('Air Canada', 'Corendon', 'Brussels airlines','KLM','LOT',
                         'Air France','Etihad Airways','Smartwings','Nordwind airlines',
                         'Transavia France','FLYONE','SkyUp','Finnair'))

model_8_Median_airlines <- lm(Price_ILS ~ Hours + airline + is_WD_4, df_filter_airlines)
summary(model_8_Median_airlines)

print(xtable(summarytst))

ols.t.stat <- summary(model_6_Median_airlines)$coef[ , "t value"]
ols.t.stat_2 <- summary(model_7_Median_airlines_Weekdays)$coef[ , "t value"]

ols.p.val  <- summary(model_6_Median_airlines)$coef[ , "Pr(>|t|)"]
ols.p.val_2  <- summary(model_7_Median_airlines_Weekdays)$coef[ , "Pr(>|t|)"]

stargazer(model_6_Median_airlines, model_7_Median_airlines_Weekdays,
          align = TRUE, no.space = TRUE, column.sep.width = '-30pt', notes.align = 'c',
          single.row = TRUE, se = list(ols.t.stat, ols.t.stat_2), p = list(ols.p.val, ols.p.val_2),
          omit.stat = c('f', 'ser'), intercept.bottom = FALSE, column.labels = c('W/O Airlines', 'With Airlines'),
          font.size = 'small')

summary(model_3_Israel_airlines_All_Weekdays)
print(xtable(tst[,c(1,2)]))

df_non_stop %>%
  group_by(airline) %>%
  mutate(price_per_hour = Price_ILS / Hours) %>%
  summarize(avg_price_per_hour = mean(price_per_hour)) %>%
  arrange(desc(airline %in% c('EL AL', 'Arkia', 'ISRAIR')), desc(airline == 'Air Sinai')) %>%
  print()
unique(df_Median_airlines$airline)
