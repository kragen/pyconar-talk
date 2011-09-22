;;; Elisp for my PyCon Ar presentation.

(defun pctalk-setup ()
  (interactive)
  (custom-set-faces
   '(default ((t (:stipple nil :background "#ffffff" 
                           :background "black" :foreground "red"
                           :inverse-video nil :box nil
                           :strike-through nil :overline nil
                           :underline nil :slant normal
                           :weight bold :height 220
                           :width normal
                           :family "courier")))
   '(mode-line ((t (:background "white" :foreground "black")))))) ; why does this fail?
  (scroll-bar-mode 0)
  (pctalk-setup-keys)
  (pctalk-resize-screen))

(defun pctalk-resize-screen ()
  (interactive)
  (shell-command "xrandr -s 640x480; xrandr -s 1024x600"))

(defun pctalk-compile-this-buffer ()
  (interactive)
  (shell-command (buffer-file-name)))

(defvar pctalk-prev-files nil
  "Currently displayed file in the presentation sequence, and previous ones.")

(defvar pctalk-next-files
  '("hello0.py" "hello1.py")
  "Files still to display in the presentation.")

(defun pctalk-next-file ()
  (interactive)
  (push (pop pctalk-next-files) pctalk-prev-files)
  (pctalk-open-current-file))

(defun pctalk-prev-file ()
  (interactive)
  (push (pop pctalk-prev-files) pctalk-next-files)
  (pctalk-open-current-file))

(defun pctalk-open-current-file ()
  (find-file (car pctalk-prev-files))
  (pctalk-compile-this-buffer))

(defun pctalk-setup-keys ()
  (interactive)
  (global-set-key (kbd "M-S-<left>") 'pctalk-prev-file)
  (global-set-key (kbd "M-S-<right>") 'pctalk-next-file)
  (global-set-key (kbd "M-S-<up>") 'pctalk-compile-this-buffer))