(defun presentation-font ()
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
  (resize-screen))
