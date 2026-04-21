if ($exitCode1 -ne 0 -or $exitCode2 -ne 0) {
    git commit -m $commitMsg
    git push origin main
    Write-Host "Successfully pushed to GitHub!" -ForegroundColor White -BackgroundColor DarkGreen
    
    # 최근 커밋에 포함된 파일 이름과 현재 로컬 수정 시간(업로드된 시간) 출력
    Write-Host "`n[Files uploaded and their modification time]" -ForegroundColor Cyan
    
    # 최근 커밋의 파일 목록을 가져와서 이름과 시간 출력
    git diff-tree --no-commit-id --name-only -r HEAD | ForEach-Object {
        $file = $_
        $time = (Get-Item $file).LastWriteTime.ToString("yyyy-MM-dd HH:mm:ss")
        Write-Host "$time | $file"
    }
} else {
    Write-Host "No changes detected to commit." -ForegroundColor Gray
}