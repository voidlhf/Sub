package main

import (
	_ "embed"
	"fmt"
	"net/http"
	"os"
	"strconv"
	"time"

	"log/slog"

	handler "github.com/xmdhs/clash2sfa/api"
)

func main() {
	// 设置端口，默认为 8090
	port := ":8090"
	if p := os.Getenv("port"); p != "" {
		port = p
	}

	// 设置日志级别
	levels := os.Getenv("level")
	leveln, err := strconv.Atoi(levels)
	if err != nil {
		leveln = -4
	}

	// 配置日志级别
	level := &slog.LevelVar{}
	level.Set(slog.Level(leveln))
	h := slog.NewJSONHandler(os.Stderr, &slog.HandlerOptions{
		Level: level,
	})

	// 创建 HTTP 服务器
	s := http.Server{
		ReadTimeout:       30 * time.Second,
		WriteTimeout:      30 * time.Second,
		ReadHeaderTimeout: 10 * time.Second,
		Addr:              port,
		Handler:           handler.SetMux(h),
	}

	// 启动 Web 服务并将其放到后台
	go func() {
		if err := s.ListenAndServe(); err != nil {
			fmt.Println("Server failed:", err)
		}
	}()

	// 主程序保持运行，不会阻塞
	select {}  // 阻塞主程序直到程序结束
}