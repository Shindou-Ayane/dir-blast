# 函数说明文档

---

## parse_arguments()
**解析命令行参数。**

**调用方式**
- **参数**
  - 无

**返回值**
- 返回解析后的命令行参数对象。

---

## run_blast(url, wordlist_path, threads, sql_scan)
**执行目录爆破和 SQL 注入扫描。**

**调用方式**
- **参数**
  - url：目标 URL 或包含 URL 的文件夹路径。
  - wordlist_path：字典文件路径。
  - threads：线程数。
  - sql_scan：是否启用 SQL 扫描。

**返回值**
- 返回扫描结果。

---

## sqlscan.py

### find_endpoints(url)
**从目标网站的首页提取所有链接作为端点。**

**调用方式**
- **参数**
  - url：目标 URL。

**返回值**
- 返回提取的端点列表。

---

### scan_sql_injection(url, endpoints, payloads)
**扫描 SQL 注入漏洞。**

**调用方式**
- **参数**
  - url：目标 URL。
  - endpoints：端点列表。
  - payloads：SQL 注入 payloads 列表。

**返回值**
- 返回存在 SQL 注入漏洞的端点列表。

---

## utils.py

### load_wordlist(file_path)
**加载字典文件。**

**调用方式**
- **参数**
  - file_path：字典文件路径。

**返回值**
- 返回字典列表。

---

### resource_path(relative_path)
**获取资源的绝对路径，适用于开发和 PyInstaller。**

**调用方式**
- **参数**
  - relative_path：相对路径。

**返回值**
- 返回资源的绝对路径。

---

## main.py

### get_common_pattern(url)
**从目标网站的首页提取常见的字符串或模式。**

**调用方式**
- **参数**
  - url：目标 URL。

**返回值**
- 返回提取的常见字符串或模式。

---

### check_directory(session, url, directory, common_pattern)
**检查目录是否存在并与常见模式进行比较。**

**调用方式**
- **参数**
  - session：aiohttp 会话对象。
  - url：目标 URL。
  - directory：要检查的目录。
  - common_pattern：常见模式。

**返回值**
- 返回存在的目录 URL 或 None。

---

### load_urls_from_folder(folder_path)
**从指定文件夹中读取所有 URL。**

**调用方式**
- **参数**
  - folder_path：文件夹路径。

**返回值**
- 返回 URL 列表。

---

### run_blast(url, wordlist_path, threads, sql_scan)
**执行目录爆破和 SQL 注入扫描。**

**调用方式**
- **参数**
  - url：目标 URL 或包含 URL 的文件夹路径。
  - wordlist_path：字典文件路径。
  - threads：线程数。
  - sql_scan：是否启用 SQL 扫描。

**返回值**
- 返回扫描结果。

---

### parse_arguments()
**解析命令行参数。**

**调用方式**
- **参数**
  - 无

**返回值**
- 返回解析后的命令行参数对象。

---

### main()
**程序入口函数。**

**调用方式**
- **参数**
  - 无

**返回值**
- 无