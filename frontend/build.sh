# 运行build命令构建静态文件
pnpm build-only
# 获取dist文件夹的绝对路径
dist_path=$(pwd)/dist

target=${1:-temp}

python -m upload $dist_path $target --private_key_path='/home/ubuntu/.ssh/id_rsa' --host='101.35.246.108'
