<?php
  class Filter {
    protected $pattern;
    protected $repl;
    function __construct($pattern, $repl) {
      $this->pattern = $pattern;
      $this->repl = $repl;
    }
    function filter($data) {
      return preg_replace($this->pattern, $this->repl, $data);
    }
  };

  class Post {
    protected $title;
    protected $text;
    protected $filters;
    function __construct($title, $text, $filters) {
      $this->title = $title;
      $this->text = $text;
      $this->filters = $filters;
    }

    function get_title() {
      return htmlspecialchars($this->title);
    }

    function display_post() {
      $text = htmlspecialchars($this->text);
      foreach ($this->filters as $filter)
        $text = $filter->filter($text);
      return $text;
    }

    function __destruct() {
      // debugging stuff
      $s = "<!-- POST " . htmlspecialchars($this->title);
      $text = htmlspecialchars($this->text);
      foreach ($this->filters as $filter)
        $text = $filter->filter($text);
      $s = $s . ": " . $text;
      $s = $s . " -->";
      echo $s;
    }
  };

  $standard_filter_set = [new Filter("/\[i\](.*)\[\/i\]/i", "<i>\\1</i>"),
                          new Filter("/\[b\](.*)\[\/b\]/i", "<b>\\1</b>"),
                          new Filter("/\[img\](.*)\[\/img\]/i", "<img src='\\1'>"),
                          new Filter("/\[br\]/i", "<br>")];
?>
