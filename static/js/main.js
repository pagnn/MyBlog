
	$(document).ready(function(){
		$('.content-markdown').each(function(){
		var content=$(this).text()
		var markedContent=marked(content)
		$(this).html(markedContent)		
		})
		$('.content-markdown img').each(function(){
		$(this).addClass('img-fluid')	
		})

		//preview content
		$('#preview-btn').click(function(event){
			event.preventDefault()
			$('#form-block').css('display','none')
			previewPost()
		})
		function previewPost(){
			var titleItem=$('#id_title')
			var contentItem=$('#id_content')
			$('#preview-block').css('display','block')
			function setContent(value){
				var markedValue=marked(value)
				$('#preview-content').html(markedValue)
				$('#preview-content img').each(function(){
				$(this).addClass('img-fluid')
				})
			}
				setContent(contentItem.val())

			function setTitle(value){
				$('#preview-title').html(value)
			}

				setTitle(titleItem.val())
		
		}
		$('#form-btn').click(function(event){
			event.preventDefault()
			$('#preview-block').css('display','none')
			$('#form-block').css('display','block')
		})
		$('.reply-btn').each(function(){
			$(this).click(function(event){
				console.log($(this))
				event.preventDefault()
				console.log($(this).parent().find('.comment-reply'))
				$(this).parent().find('.comment-reply').fadeToggle();
			})
		})
	})