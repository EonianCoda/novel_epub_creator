# 新增下載來源
  * 輕小說文庫

# 重要功能
  * discord bot: 若translate 失敗，應回傳錯誤訊息
  * 下載進度條
  * 顯示作者與簡介，方便使用者選到正確的小說
  * google drive上傳(電腦版視窗)
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