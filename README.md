# 动态脱敏工具

## 项目介绍

敏感信息假名化工具。将文档中的姓名、身份证号、手机号、邮箱、地址、机构名、统一社会信用代码替换为可逆假名，便于在不泄露真实信息的前提下进行数据共享与测试。

## 假名化原理

通过正则与 jieba 识别敏感实体，使用 PseudonymManager 为每个真实值生成确定性假名并建立双向映射表；处理文档时仅在 run 级别替换文本，保留原有格式。映射表使用 Fernet 加密落盘，支持还原。

## 假名化对象

- 姓名（NAME）
- 身份证号（ID）
- 手机号（PHONE）
- 邮箱（EMAIL）
- 地址（ADDRESS）
- 机构名（ORG）
- 统一社会信用代码（USCC）

## 映射表储存安全

映射表与密钥分别存储为 data/mapping.enc 与 data/key.bin，采用 Fernet 加密，禁止明文落盘；审计日志仅记录操作类型、敏感类型与条数，不含原文或假名。清理命令会同时删除映射表与密钥。

## 安装步骤

pip install -e .

## 运行环境

Python 3.10+（推荐 3.12/3.14），Windows / macOS / Linux。

## 使用示例

pseudo-tool anonymize sample.docx out.docx
pseudo-tool restore out.docx back.docx
pseudo-tool clear

GUI：pseudo-tool-gui\n（备用：set PYTHONPATH=src; python -m pseudo_tool.gui）

## 开发

pytest -q


## 边界测试

已覆盖：表格单元格、页眉/页脚、空文档、无敏感信息文档。

未覆盖：嵌套表格、文本框、脚注、批注、复杂样式保留。
