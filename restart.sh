
if  ps aux | grep "main.py" | grep -q "python"
then 
   echo "OK";
else
   echo "NOT OK";
   source ~/p_3_10/bin/activate
   cd /var/www/fin_assist_bot/
   nohup python main.py </dev/null &>/dev/null &
fi