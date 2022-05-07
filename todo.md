# Bug
  * encode找到的download網址(好像不是這個問題)
  * 刪除open_url的參數encoding：會有延伸問題，先保留
  * 知軒藏書search函數中search_page有可能回傳None

# 新增下載來源
  * 輕小說文庫

# 重要功能
  * Downloader中search與download以try/except處理
  * 下載進度條
  * 將來源以str紀錄，而非int，這樣在進行來源的刪減時較為方便
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
1. main.py: tab1,tab2共用相同變數output_name
2. app.py: book_dict是全域變數，當複數使用者使用時，會導致錯誤
3. app.py: 使用不同載點時，使用全域變數紀錄
4. downloader_utils.py: 若小說名稱相同時，使用dict紀錄會導致錯誤
## 複數使用者造成的問題
5. utils.download: 複數使用者下載檔案時，由於將檔案都放置於tmp下，可能會產生問題