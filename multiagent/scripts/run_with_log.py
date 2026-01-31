#!/usr/bin/env python3
"""
运行命令并将输出同步到文件
用法: python scripts/run_with_log.py <command> [--log <log_file>] [--append]
"""
import sys
import subprocess
import os
from datetime import datetime
import argparse


def run_with_log(command, log_file=None, append=False, realtime=True):
    """
    运行命令并将输出同步到文件和终端
    
    Parameters:
    -----------
    command : str or list
        要运行的命令
    log_file : str, optional
        日志文件路径，如果不指定则自动生成
    append : bool
        是否追加到日志文件（默认覆盖）
    realtime : bool
        是否实时显示输出（默认True）
    """
    # 如果没有指定日志文件，自动生成
    if log_file is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file = f'log/run_{timestamp}.log'
    
    # 确保日志目录存在
    log_dir = os.path.dirname(log_file) if os.path.dirname(log_file) else '.'
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)
    
    # 打开日志文件
    mode = 'a' if append else 'w'
    with open(log_file, mode, encoding='utf-8') as log_f:
        # 写入开始信息
        start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_f.write(f"\n{'='*80}\n")
        log_f.write(f"命令: {' '.join(command) if isinstance(command, list) else command}\n")
        log_f.write(f"开始时间: {start_time}\n")
        log_f.write(f"{'='*80}\n\n")
        log_f.flush()
        
        print(f"开始运行命令: {' '.join(command) if isinstance(command, list) else command}")
        print(f"日志文件: {log_file}")
        print(f"{'='*80}")
        
        # 运行命令
        if isinstance(command, str):
            # 字符串命令，使用 shell
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1,  # 行缓冲
                encoding='utf-8',
                errors='replace'
            )
        else:
            # 列表命令，不使用 shell
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1,
                encoding='utf-8',
                errors='replace'
            )
        
        # 实时读取输出
        try:
            for line in process.stdout:
                line = line.rstrip()
                # 同时写入日志文件和终端
                log_f.write(line + '\n')
                log_f.flush()
                if realtime:
                    print(line)
            
            # 等待进程完成
            return_code = process.wait()
            
            # 写入结束信息
            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            log_f.write(f"\n{'='*80}\n")
            log_f.write(f"结束时间: {end_time}\n")
            log_f.write(f"返回码: {return_code}\n")
            log_f.write(f"{'='*80}\n")
            log_f.flush()
            
            print(f"\n{'='*80}")
            print(f"命令执行完成，返回码: {return_code}")
            print(f"日志已保存到: {log_file}")
            
            return return_code
            
        except KeyboardInterrupt:
            # 处理 Ctrl+C
            process.terminate()
            process.wait()
            log_f.write(f"\n\n[!] 命令被用户中断 (Ctrl+C)\n")
            log_f.flush()
            print(f"\n[!] 命令被中断，日志已保存到: {log_file}")
            return 130  # Ctrl+C 的标准返回码


def main():
    parser = argparse.ArgumentParser(
        description='运行命令并将输出同步到文件',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 方式1: 使用引号包裹整个命令（推荐）
  python scripts/run_with_log.py "python main_PACE.py --args" --log output/training.log
  
  # 方式2: 使用 -- 分隔选项和命令
  python scripts/run_with_log.py --log output/training.log -- python main_PACE.py --args
  
  # 方式3: 选项在前，命令在后（如果命令中没有 --log 等选项）
  python scripts/run_with_log.py --log output/training.log python main_PACE.py --args
  
  # 追加到现有日志文件
  python scripts/run_with_log.py "python main_PACE.py" --log output/training.log --append
  
  # 不实时显示输出（只保存到文件）
  python scripts/run_with_log.py "python main_PACE.py" --log output/training.log --no-realtime
        """
    )
    
    parser.add_argument(
        '--log', '-l',
        type=str,
        default=None,
        help='日志文件路径（默认: log/run_YYYYMMDD_HHMMSS.log）'
    )
    parser.add_argument(
        '--append', '-a',
        action='store_true',
        help='追加到日志文件而不是覆盖'
    )
    parser.add_argument(
        '--no-realtime',
        action='store_true',
        help='不实时显示输出（只保存到文件）'
    )
    
    # 检查是否有 -- 分隔符
    if '--' in sys.argv:
        sep_idx = sys.argv.index('--')
        # -- 之前是选项，之后是命令
        known_args, unknown_args = parser.parse_known_args(sys.argv[1:sep_idx])
        command = sys.argv[sep_idx + 1:]
    else:
        # 没有 -- 分隔符，尝试解析
        known_args, unknown_args = parser.parse_known_args()
        # unknown_args 应该是命令部分
        command = unknown_args
    
    if not command:
        parser.print_help()
        sys.exit(1)
    
    # 如果只有一个参数且包含空格，当作字符串命令处理
    if len(command) == 1 and ' ' in command[0]:
        command = command[0]
    
    return_code = run_with_log(
        command,
        log_file=known_args.log,
        append=known_args.append,
        realtime=not known_args.no_realtime
    )
    
    sys.exit(return_code)


if __name__ == '__main__':
    main()