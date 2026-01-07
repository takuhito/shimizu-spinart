# Antigravity Global Instructions - Project Structure & MTML

## グローバル・運用ルール（すべてのワークスペース共通）

今後、どのプロジェクト・ワークスペースにおいても、以下のルールを私の**標準仕様**として適用します。

1.  **新規フォルダの作成**: 各プログラムや作業単位ごとに、日付やプロジェクト名を含んだ新規フォルダを作成する。
3.  **拡張子の使い分け**:
    *   通常のHTMLファイル: `.html`
    *   MovableType テンプレート（MTML）: `.mtml`
    *   **MTML 開発環境**: VS Code 拡張機能 「Movable Type (yupyom.mtml)」の使用を推奨。
    *   **フォーマッタ対策**: `settings.json` で `[mtml]` に対して `editor.formatOnSave: false` を設定する。
4.  **README.md の作成**: 作成した新規フォルダの中に必ず `README.md` を作成する。
5.  **ドキュメントの充実**: `README.md` には以下の内容を含める。
    *   プログラムの内容・概要
    *   修正内容・履歴
    *   依頼主への連絡用テキスト（必要に応じて）
