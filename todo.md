# 近期需求
  * config檔，紀錄使用者設定，如預設輸出路徑，選擇路徑，選項設定
  * 批量轉換支援rar,zip
  * 黑名單改成用選取的刪除
  * 輕小說文庫：後記中經常出現滿足正規表達式的句子，可以擋掉
  * 輕小說文庫：顯示該小說網址
  * 輕小說文庫：去爬章節名稱
  
# 新增下載來源
  * 哔哩轻小说

# 重要功能
  * discord bot: 若translate 失敗，應回傳錯誤訊息
  * 下載進度條
  * 顯示作者與簡介，方便使用者選到正確的小說
  * google drive上傳(電腦版視窗)image.png
  * 中國網路小說/輕小說 選擇
  * 搜尋google drive已有檔案
  * discord button

# 額外功能
  * 譯名轉換
  * 讓使用者切換來源
  * 讀取epub簡繁轉換

# 潛在問題
  * main.py: tab1,tab2共用相同變數output_name
  * downloader_utils.py: 若小說名稱相同時，使用dict紀錄會導致錯誤
## 複數使用者造成的問題
  * utils.download: 複數使用者下載檔案時，由於將檔案都放置於tmp下，可能會產生問題