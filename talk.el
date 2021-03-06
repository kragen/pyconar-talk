;;; Elisp for my PyCon Ar presentation.

(defun pctalk-setup ()
  "Set up the PyCon talk."
  (interactive)
  (custom-set-faces
   '(default ((t (:stipple nil :background "#ffffff" 
                           :background "black" :foreground "red"
                           :inverse-video nil :box nil
                           :strike-through nil :overline nil
                           :underline nil :slant normal
                           :weight bold :height 300
                           :width normal
                           :family "courier"))))
   '(mode-line ((t (:background "#001111" :foreground "#770000")))))
  (scroll-bar-mode 0)
  (pctalk-setup-keys)
  (pctalk-resize-screen))

(defun pctalk-resize-screen ()
  "Resize the screen a couple of times to work around an Emacs bug."
  (interactive)
  (shell-command "xrandr -s 640x480")
  (pctalk-maxsize-screen))

(defun pctalk-maxsize-screen ()
  "Resize the screen to max size to work around Emacs or SDL bugs."
  (interactive)
  (shell-command "xrandr -s \"$(xrandr | head -3 | tail -1 | awk '{print $1}')\""))

(defun pctalk-compile-this-buffer ()
  "Execute the script in the current buffer in the shell."
  (interactive)
  (save-buffer)
  (shell-command (buffer-file-name))
  (pctalk-maxsize-screen))

;;; These two stacks of filenames form a sequence of files you can
;;; move back and forth along with pctalk-prev-file and
;;; pctalk-next-file.  I tried doing it with a single list and an
;;; index into the list, but it was just a bad scene.

(defconst pctalk-prev-files nil
  "Currently displayed file in the presentation sequence, and previous ones.")

(defconst pctalk-next-files
  '("helloneg1.py" "hellonegmedio.py" "hellonegcuarto.py"
    "hello0.py" "hello1.py"
    "polygons.py"
    "circles.py"
    "reloj.py"
    "sintesis0.py" "sintesis1.py" "sintesis2.py"
    "ondas.py" "klappquadrat.py"
    "pygmusic.py")
  "Files still to display in the presentation.")

(defmacro pctalk-pop (place)
  "Like pop, but errors if place is nil."
  (if (not (symbolp place)) (error "popping nonsymbols unimplemented"))
  `(if ,place (car (prog1 
                       ,place 
                       (setq ,place (cdr ,place))))
     (error "popping from empty stack %S" ',place)))

(defun pctalk-next-file ()
  "Go to next file in presentation and run it."
  (interactive)
  (push (pctalk-pop pctalk-next-files) pctalk-prev-files)
  (pctalk-open-current-file))

(defun pctalk-prev-file ()
  "Go to previous file in presentation and run it."
  (interactive)
  (push (pctalk-pop pctalk-prev-files) pctalk-next-files)
  (if pctalk-prev-files 
      (pctalk-open-current-file)
    (message "Back past first file.")))

(defun pctalk-open-current-file ()
  (find-file (car pctalk-prev-files))
  (delete-other-windows)
  (pctalk-compile-this-buffer))

(defun pctalk-setup-keys ()
  (interactive)
  (global-set-key (kbd "M-S-<left>") 'pctalk-prev-file)
  (global-set-key (kbd "M-S-<right>") 'pctalk-next-file)
  (global-set-key (kbd "M-S-<up>") 'pctalk-compile-this-buffer))
